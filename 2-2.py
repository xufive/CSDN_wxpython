#!/usr/bin/env python
# coding:utf-8

import os
import wx

class MainFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "wxPython控件演示", style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize((780, 450)) # wx.Frame用于设置窗口大小的方法
        self.Center() # wx.Frame用于设置窗口屏幕居中的方法

        # 创建一个面板，用于放置控件
        panel = wx.Panel(self, -1)

        # 创建静态文本控件
        self.notice = wx.StaticText(panel, -1, "Hello wxPython", pos=(20, 20))

        # 创建静态图片控件，并绑定鼠标左键点击事件
        bmp = wx.Bitmap(os.path.join("res", "forever.png"))
        sb = wx.StaticBitmap(panel, -1, bmp, pos=(280, 10))
        sb.Bind(wx.EVT_LEFT_DOWN, self.OnBitmapLeftDown)           # 鼠标左键按下事件
        sb.Bind(wx.EVT_LEFT_UP, self.OnBitmapLeftUp)               # 鼠标左键抬起事件
        sb.Bind(wx.EVT_LEFT_DCLICK, self.OnBitmapLeftDclick)       # 鼠标左键双击事件

        sb.Bind(wx.EVT_RIGHT_DOWN, self.OnBitmapRightDown)         # 鼠标右键按下事件
        sb.Bind(wx.EVT_RIGHT_UP, self.OnBitmapRightUp)             # 鼠标右键抬起事件
        sb.Bind(wx.EVT_RIGHT_DCLICK, self.OnBitmapRightDclick)     # 鼠标右键双击事件

        sb.Bind(wx.EVT_MOTION, self.OnBitmapMotion)                # 鼠标移动事件
        sb.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveBitmapWindow)     # 鼠标移出事件
        sb.Bind(wx.EVT_MOUSEWHEEL, self.OnBitmapMouseWheel)        # 鼠标滚轮事件

        # 创建文本输入框，并绑定输入变化事件
        tc1 = wx.TextCtrl(panel, -1, pos=(20, 50), size=(260, -1), name="输入框")
        tc1.Bind(wx.EVT_TEXT, self.OnTextChange)

        # 创建密码输入框，并使用第二种方式绑定
        tc2 = wx.TextCtrl(panel, -1, pos=(20, 90), style=wx.TE_PASSWORD, name="密码输入框")
        self.Bind(wx.EVT_TEXT, self.OnTextChange, tc2)

        # 创建单选按钮，并绑定选择事件
        rb1 = wx.RadioButton(panel, -1, "单选按钮1", pos=(20, 130), style=wx.RB_GROUP, name="rb1")
        rb1.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)

        # 创建单选按钮，并绑定选择事件
        rb2 = wx.RadioButton(panel, -1, "单选按钮2", pos=(100, 130), name="rb2")
        rb2.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)

        # 创建单选按钮，并绑定选择事件
        rb3 = wx.RadioButton(panel, -1, "单选按钮3", pos=(180, 130), name="rb3")
        rb3.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
        
        # 创建复选按钮，并绑定选择事件
        cb1 = wx.CheckBox(panel, -1, "复选按钮", pos=(20, 160))
        cb1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

        # 创建复选按钮，并绑定选择事件
        cb2 = wx.CheckBox(panel, -1, "文字在左侧的复选按钮", pos=(100, 160), style=wx.ALIGN_RIGHT)
        cb2.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

        # 创建按钮，并绑定按钮事件
        btn = wx.Button(panel, -1, "按钮", pos=(20, 190))
        btn.Bind(wx.EVT_BUTTON, self.OnButton)

        # 创建多行文本框，显示触发的事件
        self.evtlog = wx.TextCtrl(panel, -1, pos=(20, 230), size=(260, 150), style=wx.TE_MULTILINE | wx.CB_READONLY)

        # 为MainFrame绑定窗口最大化事件
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximize)

    def OnBitmapLeftDown(self, evt):
        """左键按下事件处理"""

        self.evtlog.AppendText("左键按下\n")

    def OnBitmapLeftUp(self, evt):
        """左键抬起事件处理"""

        self.evtlog.AppendText("左键抬起\n")

    def OnBitmapLeftDclick(self, evt):
        """左键双击事件处理"""

        self.evtlog.AppendText("左键双击\n")

    def OnBitmapRightDown(self, evt):
        """右键按下事件处理"""

        self.evtlog.AppendText("右键按下\n")

    def OnBitmapRightUp(self, evt):
        """右键抬起事件处理"""

        self.evtlog.AppendText("右键抬起\n")

    def OnBitmapRightDclick(self, evt):
        """右键双击事件处理"""

        self.evtlog.AppendText("右键双击\n")

    def OnBitmapMotion(self, evt):
        """鼠标移动事件处理"""

        self.notice.SetLabel("x:%03d y:%03d" % (evt.x, evt.y))

    def OnLeaveBitmapWindow(self, evt):
        """鼠标移出图片事件处理"""

        self.notice.SetLabel("Hello wxPython")
    
    def OnBitmapMouseWheel(self, evt):
        """鼠标滚轴事件处理"""

        if evt.WheelRotation > 0:
            self.evtlog.AppendText("滚轮向上\n")
        else:
            self.evtlog.AppendText("滚轮向下\n")

    def OnTextChange(self, evt):
        """文本框输入变化事件处理"""

        name = evt.GetEventObject().GetName()
        text = evt.GetString()
        self.evtlog.AppendText("%s: %s\n" % (name, text))

    def OnRadioButton(self, evt):
        """单选按钮选择事件处理"""

        label = evt.GetEventObject().GetLabel()
        self.evtlog.AppendText("%s:被选中\n" % label)

    def OnCheckBox(self, evt):
        """复选按钮勾选事件处理"""

        obj = evt.GetEventObject()
        label = obj.GetLabel()
        status = "勾选" if obj.GetValue() else "取消"
        self.evtlog.AppendText("%s:被%s\n" % (label, status))

    def OnButton(self, evt):
        """按钮点击事件处理"""

        self.evtlog.AppendText("按钮被点击\n")

    def OnMaximize(self, evt):
        """窗口最大化事件"""

        self.evtlog.AppendText("窗口最大化\n")

class MainApp(wx.App):

    def OnInit(self):

        self.SetAppName("Hello World")
        self.frame = MainFrame(None)
        self.frame.Show()

        return True

def main():
    app = MainApp()
    app.MainLoop()
   
if __name__ == '__main__':
    main()


    