#!/usr/bin/env python
# coding:utf-8

import wx

class MainFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "Hello World", 
            size=(800, 600), style=wx.DEFAULT_FRAME_STYLE)

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
