#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用wxPython制作二维码生成器
"""

import os
import wx
import wx.lib.filebrowsebutton as filebrowse
import wx.lib.colourselect as csel
from PIL import Image
import qrcode

APP_TITLE = "二维码生成器"
WILDCARD = "PNG(*.png)|*.png|JPG(*.jpg)|*.jpg"

# ================================================================================
class MainFrame(wx.Frame):
    """主窗口"""

    # --------------------------------------------------------------------------------
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, -1, APP_TITLE, size=(800, 500),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        # 设置图标
        icon = wx.Icon(os.path.join("res", "QrCreator.ico"))
        self.SetIcon(icon)

        # 窗口布局
        # 顶级Panel
        panel = wx.Panel(self, -1)

        # 顶级Sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧Panel
        leftPanel = wx.Panel(panel, -1)
        sizer.Add(leftPanel, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, border=20)    # 加入Sizer

        # 分隔线
        line = wx.StaticLine(panel, -1, style=wx.VERTICAL)
        sizer.Add(line, 0, wx.EXPAND | wx.ALL, border=10)   # 加入Sizer

        # 右侧Panel
        rightPanel = wx.Panel(panel, -1)
        sizer.Add(rightPanel, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, border=20)   # 加入Sizer

        # 界面总成
        panel.SetSizer(sizer)
        panel.Layout()

        # 初始化左侧Panel
        self.InitLeftPanel(leftPanel)

        # 初始化右侧Panel
        self.InitRightPanel(rightPanel)

        self.CenterOnScreen()

    # --------------------------------------------------------------------------------
    def InitLeftPanel(self, panel):
        """
        初始化左侧窗口

        :param panel: 左侧Panel
        """

        # 使用GridBagSizer布局左侧窗口
        sizer = wx.GridBagSizer(5, 5)     # 参数的意义是Sizer内的控件之间横向和纵向的像素间隔

        # 二维码文本输入框
        text = wx.StaticText(panel, -1, "文本：")
        sizer.Add(text, (0, 0))
        self.tc = wx.TextCtrl(panel, -1, "", style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        sizer.Add(self.tc, (1, 0), (1, 2), flag=wx.EXPAND)

        # 二维码大小滑块
        text = wx.StaticText(panel, -1, "大小：")
        sizer.Add(text, (2, 0), flag=wx.TOP, border=5)
        self.size = wx.Slider(panel, -1, 1, 1, 5, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        sizer.Add(self.size, (3, 0), flag=wx.EXPAND)

        # 二维码容错标准
        text = wx.StaticText(panel, -1, "容错：")
        sizer.Add(text, (2, 1), flag=wx.TOP, border=5)
        choices = [
            "低：约修正7%的错误",
            "中：约修正15%的错误",
            "高：约修正30%的错误"
        ]
        self.tolerance = wx.Choice(panel, -1, choices=choices)
        self.tolerance.SetSelection(1)      # 默认选中“中”
        sizer.Add(self.tolerance, (3, 1), flag=wx.EXPAND)

        # 二维码中间logo
        text = wx.StaticText(panel, -1, "logo：")
        sizer.Add(text, (4, 0), flag=wx.TOP, border=5)
        self.logo = filebrowse.FileBrowseButton(panel, -1, labelText="", buttonText="浏览", toolTip="请选择二维码Logo",
                                                dialogTitle="二维码Logo", fileMask=WILDCARD,
                                                changeCallback=self.ShowQrCode)
        sizer.Add(self.logo, (5, 0), (1, 2), flag=wx.EXPAND)

        # 二维码颜色
        staticBox = wx.StaticBox(panel, -1, "颜色：")
        sbSizer = wx.StaticBoxSizer(staticBox)
        innerSizer = wx.BoxSizer()      # 为了实现空白间隔，再套一层BoxSizer
        text = wx.StaticText(panel, -1, "前景：")
        innerSizer.Add(text, 0)
        self.fgColor = csel.ColourSelect(panel, -1, colour=wx.BLACK)
        innerSizer.Add(self.fgColor, 1, wx.RIGHT, 5)
        text = wx.StaticText(panel, -1, "背景：")
        innerSizer.Add(text, 0, flag=wx.LEFT, border=5)
        self.bgColor = csel.ColourSelect(panel, -1, colour=wx.WHITE)
        innerSizer.Add(self.bgColor, 1)
        sbSizer.Add(innerSizer, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(sbSizer, (6, 0), (1, 2), flag=wx.EXPAND)

        # 总成
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1)
        panel.SetSizer(sizer)
        panel.Layout()

        # 绑定事件
        self.tc.Bind(wx.EVT_TEXT, self.ShowQrCode)
        self.size.Bind(wx.EVT_SLIDER, self.ShowQrCode)
        self.tolerance.Bind(wx.EVT_CHOICE, self.ShowQrCode)
        self.fgColor.Bind(csel.EVT_COLOURSELECT, self.ShowQrCode)
        self.bgColor.Bind(csel.EVT_COLOURSELECT, self.ShowQrCode)

        # 颜色选择控件需要响应一下大小变化事件，才能有较好的显示效果
        self.fgColor.Bind(wx.EVT_SIZE, self.OnFgColorSizeChange)
        self.bgColor.Bind(wx.EVT_SIZE, self.OnBgColorSizeChange)

    # --------------------------------------------------------------------------------
    def OnFgColorSizeChange(self, evt):
        """前景色选择控制大小事件处理"""

        self.fgColor.SetColour(wx.BLACK)

    # --------------------------------------------------------------------------------
    def OnBgColorSizeChange(self, evt):
        """背景色选择控制大小事件处理"""

        self.bgColor.SetColour(wx.WHITE)

    # --------------------------------------------------------------------------------
    def InitRightPanel(self, panel):
        """
        初始化右侧窗口

        :param panel: 右侧Panel
        """

        sizer = wx.GridBagSizer(10, 10)

        # 静态图片
        bitWindow = wx.ScrolledWindow(panel, -1, style=wx.BORDER_SUNKEN)
        bitWindow.SetBackgroundColour(wx.WHITE)
        bitWindow.SetScrollRate(20, 20)

        self.bitmap = wx.StaticBitmap(bitWindow, -1)
        self.bitmap.SetBackgroundColour(wx.WHITE)
        self.bitmap.CenterOnParent()

        sizer.Add(bitWindow, (0, 0), (1, 2), wx.EXPAND)

        # 保存到文件
        fileBtn = wx.Button(panel, -1, "保存到文件")
        sizer.Add(fileBtn, (1, 0), flag=wx.EXPAND)

        # 复制到剪切板
        clipboardBtn = wx.Button(panel, -1, "复制到剪切板")
        sizer.Add(clipboardBtn, (1, 1), flag=wx.EXPAND)

        # 总成
        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        panel.SetSizer(sizer)

        # 绑定事件
        fileBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        clipboardBtn.Bind(wx.EVT_BUTTON, self.OnClipBoard)

    # --------------------------------------------------------------------------------
    def OnSave(self, evt):
        """保存二维码到文件"""

        if len(self.tc.GetValue()) > 0:
            dlg = wx.FileDialog(
                self, message="保存二维码文件", defaultDir=os.getcwd(),
                defaultFile="qrcode.png", wildcard=WILDCARD, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if os.path.splitext(path)[1].lower() == ".png":
                    imgType = wx.BITMAP_TYPE_PNG
                else:
                    imgType = wx.BITMAP_TYPE_JPEG

                self.bitmap.GetBitmap().SaveFile(path, imgType)

    # --------------------------------------------------------------------------------
    def OnClipBoard(self, evt):
        """复制二维码到剪切板事件处理"""

        if len(self.tc.GetValue()) > 0:
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.BitmapDataObject(self.bitmap.GetBitmap()))
                wx.TheClipboard.Close()

                wx.MessageDialog(self, "成功复制到剪切板。", APP_TITLE, wx.OK | wx.ICON_INFORMATION).ShowModal()
            else:
                wx.MessageDialog(self, "访问剪切板失败。", APP_TITLE, wx.OK | wx.ICON_ERROR).ShowModal()

    # --------------------------------------------------------------------------------
    def ShowQrCode(self, evt):
        """显示二维码"""

        text = self.tc.GetValue()
        if len(text) > 0:
            # 初始化qrcode
            ec = [qrcode.constants.ERROR_CORRECT_L, qrcode.constants.ERROR_CORRECT_M, qrcode.constants.ERROR_CORRECT_H]
            qr = qrcode.QRCode(
                version=self.size.GetValue(),
                error_correction=ec[self.tolerance.GetSelection()]
            )

            # 设置二维码文本
            qr.add_data(text)

            # 生成二维码图片
            img = qr.make_image(fill_color=self.fgColor.GetValue().GetAsString(),
                                back_color=self.bgColor.GetValue().GetAsString())

            # 设置二维码Logo
            logoPath = self.logo.GetValue()
            if len(logoPath) > 0 and os.path.isfile(logoPath):
                img = img.convert("RGB")
                icon = Image.open(logoPath)

                # 获取图片的宽高
                img_w, img_h = img.size

                # 参数设置logo的大小
                factor = 4
                size_w = int(img_w / factor)
                size_h = int(img_h / factor)
                icon_w, icon_h = icon.size
                if icon_w > size_w:
                    icon_w = size_w
                if icon_h > size_h:
                    icon_h = size_h

                # 重新设置logo的尺寸
                icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

                # 得到画图的x，y坐标，居中显示
                w = int((img_w - icon_w) / 2)
                h = int((img_h - icon_h) / 2)

                # 黏贴logo照
                img.paste(icon, (w, h), mask=None)

            # 显示二维码
            self.bitmap.SetBitmap(wx.Bitmap(self._PIL2Wx(img)))
            self.bitmap.GetParent().SetVirtualSize(self.bitmap.GetSize())
            self.bitmap.CenterOnParent()

    # --------------------------------------------------------------------------------
    @staticmethod
    def _PIL2Wx(pilimg):
        """将PIL Image对象转换为wx.Image"""

        image = wx.Image(pilimg.size[0], pilimg.size[1])
        image.SetData(pilimg.convert("RGB").tobytes())

        return image


# ================================================================================
class MainApp(wx.App):
    """主应用程序"""

    # --------------------------------------------------------------------------------
    def OnInit(self):
        """
        主应用程序初始化回调函数
        :return: True
        """

        self.SetAppName(APP_TITLE)
        self.frame = MainFrame(None)
        self.frame.Show()

        return True


# --------------------------------------------------------------------------------
def main():
    """主函数"""

    app = MainApp()
    app.MainLoop()


# ================================================================================
if __name__ == "__main__":
    main()
