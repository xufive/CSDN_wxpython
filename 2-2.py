#!/usr/bin/env python
# coding:utf-8

import os
import wx

class MainFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "wxPython控件演示", 
            size=(780, 450), style=wx.DEFAULT_FRAME_STYLE)

        # 创建一个面板，用于放置控件
        panel = wx.Panel(self, -1)

        # 创建静态文本控件
        st = wx.StaticText(panel, -1, "Hello wxPython", pos=(20, 20))

        # 创建静态图片控件，并绑定鼠标左键点击事件
        bmp = wx.Bitmap(os.path.join("res", "forever.png"))
        sb = wx.StaticBitmap(panel, -1, bmp, pos=(280, 10))
        sb.Bind(wx.EVT_LEFT_DOWN, self.OnBitmapClick)

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

    def OnBitmapClick(self, evt):
        """在StaticBitmap控件上点击左键事件处理"""

        self.evtlog.AppendText("左键点击图片\n")

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


    