#!/usr/bin/env python
# coding:utf-8

"""
wxPython鼠标事件例程
"""

import wx

APP_TITLE = "Hello World"


class MainFrame(wx.Frame):
    """主框架"""

    def __init__(self, parent):
        """
        主框架构造函数

        :param parent: 父窗口
        """

        # 初始化父类
        wx.Frame.__init__(self, parent, -1, APP_TITLE, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE)

        # 初始化面板
        panel = wx.Panel(self, -1)

        # 初始化窗口控件
        text = wx.StaticText(panel, -1, "在此区域内进行鼠标操作", pos=(330, 280))

        # 设置状态栏
        self.sb = wx.StatusBar(self, -1)
        self.sb.SetFieldsCount(3)               # 将状态栏分为三个部分
        self.sb.SetStatusWidths([-3, -1, -1])   # 按比例分隔

        self.sb.SetStatusText("就绪", 0)
        self.sb.SetStatusText("X:---", 1)
        self.sb.SetStatusText("Y:---", 2)

        self.SetStatusBar(self.sb)

        # 绑定事件
        panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)           # 鼠标左键按下事件
        panel.Bind(wx.EVT_LEFT_UP, self.OnLeftUP)               # 鼠标左键抬起事件
        panel.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDclick)       # 鼠标左键双击事件

        panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)         # 鼠标右键按下事件
        panel.Bind(wx.EVT_RIGHT_UP, self.OnRightUP)             # 鼠标右键抬起事件
        panel.Bind(wx.EVT_RIGHT_DCLICK, self.OnRightDclick)     # 鼠标右键双击事件

        panel.Bind(wx.EVT_MOTION, self.OnMotion)                # 鼠标移动事件
        panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)     # 鼠标移出事件
        panel.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)        # 鼠标滚轮事件

    def OnLeftDown(self, evt):
        """左键按下事件处理"""
        self.sb.SetStatusText("左键按下", 0)

    def OnLeftUP(self, evt):
        """左键抬起事件处理"""
        self.sb.SetStatusText("左键抬起", 0)

    def OnLeftDclick(self, evt):
        """左键双击事件处理"""
        self.sb.SetStatusText("左键双击", 0)

    def OnRightDown(self, evt):
        """右键按下事件处理"""
        self.sb.SetStatusText("右键按下", 0)

    def OnRightUP(self, evt):
        """右键抬起事件处理"""
        self.sb.SetStatusText("右键抬起", 0)

    def OnRightDclick(self, evt):
        """右键双击事件处理"""
        self.sb.SetStatusText("右键双击", 0)

    def OnMotion(self, evt):
        """鼠标移动事件处理"""
        self.sb.SetStatusText("X:%03d" % evt.x, 1)
        self.sb.SetStatusText("Y:%03d" % evt.y, 2)

    def OnLeaveWindow(self, evt):
        """鼠标移出事件处理"""
        self.sb.SetStatusText("X:---", 1)
        self.sb.SetStatusText("Y:---", 2)

    def OnMouseWheel(self, evt):
        """鼠标滚轮事件处理"""

        if evt.WheelRotation > 0:
            self.sb.SetStatusText("滚轮向上", 0)
        else:
            self.sb.SetStatusText("滚轮向下", 0)


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