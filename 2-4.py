#!/usr/bin/env python
# coding:utf-8

import wx

class MainFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "Hello World", 
            size=(800, 600), style=wx.DEFAULT_FRAME_STYLE)

        # 创建一个面板，用于放置控件
        panel = wx.Panel(self, -1)

        # 创建打开文件按钮
        openbtn = wx.Button(panel, -1, "打开文件", pos=(20, 20))
        openbtn.Bind(wx.EVT_BUTTON, self.OnOpenFile)

        # 创建字体设置按钮
        fontbtn = wx.Button(panel, -1, "设置字体", pos=(110, 20))
        fontbtn.Bind(wx.EVT_BUTTON, self.OnFont)

        # 创建文本编辑控件 
        self.tc = wx.TextCtrl(panel, -1, pos=(20, 60), size=(740, 480), style=wx.TE_MULTILINE | wx.TE_RICH2)
        self.tc.Enable(False)

    def OnOpenFile(self, evt):
        """打开文件事件处理"""

        # 创建文件打开对话框
        dlg = wx.FileDialog(self, "打开文件", wildcard="文本文件|*.txt")

        # 以模态方式打开对话框
        if dlg.ShowModal() == wx.ID_OK:
            self.file = dlg.GetPath()       # 取得选择的文件路径
            self.tc.LoadFile(self.file)     # 加载文件
            self.tc.Enable(True)            # 设置文本框可用

    
    def OnFont(self, evt):
        """字体设置事件处理"""

        # 取得当前字体
        curFont = self.tc.GetFont()
        
        # 设置字体数据
        fontData = wx.FontData()
        fontData.SetInitialFont(curFont)

        # 创建字体选择对话框
        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            # 取得选中的字体
            data = dlg.GetFontData()
            font = data.GetChosenFont()

            # 将字体应用到文本框
            self.tc.SetFont(font)

            # 取得颜色设置
            colour = data.GetColour()

            # 将颜色应用于文本框
            self.tc.SetForegroundColour(colour)

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
