#!/usr/bin/env python
# coding:utf-8

"""
wxPython桌面程序模板
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
        wx.Frame.__init__(self, parent, -1, APP_TITLE, size=(600, 400), style=wx.DEFAULT_FRAME_STYLE)

        # 初始化面板
        panel = wx.Panel(self, -1)

        # 初始化布局管理器
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 创建控件并添加到布局管理器中
        st1 = wx.StaticText(panel, -1, "one", style=wx.BORDER_SIMPLE)
        sizer.Add(st1, 0, wx.ALIGN_CENTRE)

        st2 = wx.StaticText(panel, -1, "two", style=wx.BORDER_SIMPLE)
        sizer.Add(st2, 1, wx.EXPAND)

        st3 = wx.StaticText(panel, -1, "three", style=wx.BORDER_SIMPLE)
        sizer.Add(st3, 2, wx.EXPAND | wx.TOP | wx.BOTTOM, 20)

        st4 = wx.StaticText(panel, -1, "four", style=wx.BORDER_SIMPLE)
        sizer.Add(st4, 2, wx.EXPAND | wx.ALL, 20)

        # 创建子Sizer
        subSizer = wx.BoxSizer(wx.VERTICAL)

        # 向子Sizer中加入控件
        st5 = wx.StaticText(panel, -1, "five", style=wx.BORDER_SIMPLE)
        subSizer.Add(st5, 1, wx.EXPAND)

        st6 = wx.StaticText(panel, -1, "six", style=wx.BORDER_SIMPLE)
        subSizer.Add(st6, 1, wx.EXPAND)

        st7 = wx.StaticText(panel, -1, "seven", style=wx.BORDER_SIMPLE)
        subSizer.Add(st7, 1, wx.EXPAND)

        # 将子Sizer加入Sizer中
        sizer.Add(subSizer, 1, wx.EXPAND)

        # 为面板指定布局管理器
        panel.SetSizer(sizer)

        # 布局
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