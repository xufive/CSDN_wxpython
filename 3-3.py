#!/usr/bin/env python
# coding:utf-8

"""
wxPython桌面程序模板
"""

import os
import wx

APP_TITLE = "用户注册"


class MainFrame(wx.Frame):
    """主框架"""

    def __init__(self, parent):
        """
        主框架构造函数

        :param parent: 父窗口
        """

        # 初始化父类
        wx.Frame.__init__(self, parent, -1, APP_TITLE, size=(650, 470), style=wx.DEFAULT_FRAME_STYLE)

        # 初始化面板
        panel = wx.Panel(self, -1)

        # 初始化Sizer
        sizer = wx.GridBagSizer(10, 10)     # 每个控件之间横纵间隔10像素
        
        # 用户名
        st = wx.StaticText(panel, -1, "用户名")
        sizer.Add(st, (0, 0), flag=wx.TOP | wx.ALIGN_RIGHT, border=20)     # 在第0行0列，距离上边缘20像素，居右

        userName = wx.TextCtrl(panel, -1)
        sizer.Add(userName, (0, 1), (1, 3), flag=wx.EXPAND | wx.TOP, border=20)         # 在第0行1列，跨3列，距离上边缘20像素

        # 二维码，在第0行4列，跨7行，距离上、右边缘20像素
        sb = wx.StaticBitmap(panel, -1, wx.Bitmap(os.path.join("res", "qrcode.png")))
        sizer.Add(sb, (0, 5), (7, 1), flag=wx.TOP | wx.RIGHT, border=20)

        # 密码
        st = wx.StaticText(panel, -1, "密码")
        sizer.Add(st, (1, 0), flag=wx.ALIGN_RIGHT)      # 在第1行0列，居右

        password = wx.TextCtrl(panel, -1, style=wx.TE_PASSWORD)
        sizer.Add(password, (1, 1), (1, 3), flag=wx.EXPAND)     # 在第1行1列，跨3列

        # 学历
        st = wx.StaticText(panel, -1, "学历")
        sizer.Add(st, (2, 0), flag=wx.ALIGN_RIGHT)      # 在第2行0列，居右

        level1 = wx.RadioButton(panel, -1, "专科")
        sizer.Add(level1, (2, 1))      # 在第2行1列

        level2 = wx.RadioButton(panel, -1, "本科")
        sizer.Add(level2, (2, 2))      # 在第2行1列

        level3 = wx.RadioButton(panel, -1, "研究生及以上")
        sizer.Add(level3, (2, 3))      # 在第2行1列

        # 职业
        st = wx.StaticText(panel, -1, "职业")
        sizer.Add(st, (3, 0), flag=wx.ALIGN_RIGHT)      # 在第3行0列，居右

        professional = wx.Choice(panel, -1, choices=["学生", "程序员", "软件工程师", "系统架构师"])
        professional.SetSelection(0)
        sizer.Add(professional, (3, 1), (1, 3), flag=wx.EXPAND)     # 在第3行1列，跨3列

        # 语言技能
        st = wx.StaticText(panel, -1, "语言技能")
        sizer.Add(st, (4, 0), flag=wx.ALIGN_RIGHT | wx.LEFT, border=20)      # 在第4行0列，距离左边缘20像素，居右

        choices = ["C", "C++", "Java", "Python", "Lua", "JavaScript", "TypeScript", "Go", "Rust"]
        language = wx.ListBox(panel, -1, choices=choices, style=wx.LB_EXTENDED)
        sizer.Add(language, (4, 1), (1, 3), flag=wx.EXPAND)     # 在第4行1列，跨3列

        # 是否入群
        isJoin = wx.CheckBox(panel, -1, "已加入QQ群", style=wx.ALIGN_RIGHT)
        sizer.Add(isJoin, (5, 0), (1, 4), flag=wx.ALIGN_CENTER)     # 在第5行0列，跨4列, 居中

        # 提交
        btn = wx.Button(panel, -1, "提交")
        sizer.Add(btn, (6, 0), (1, 4), flag=wx.ALIGN_CENTER)     # 在第6行0列，跨4列, 居中

        # 界面总成
        sizer.AddGrowableRow(4)     # 设置第4行可增长
        sizer.AddGrowableCol(3)     # 设置第3列可增长
        panel.SetSizer(sizer)
        panel.Layout()


class MainApp(wx.App):
    """主应用程序"""

    def OnInit(self):
        """主应用程序初始化回调函数"""

        self.SetAppName(APP_TITLE)
        self.frame = MainFrame(None)
        self.frame.Show()

        return True

    def GetMainFrame(self):
        """取得主框架"""

        return self.frame


def main(debug=True):
    if debug:
        fp = open("debug.txt", "w")
        fp.close()
        app = MainApp(redirect=True, filename="debug.txt")
    else:
        app = MainApp()

    app.MainLoop()

   
if __name__ == '__main__':
    main(False)