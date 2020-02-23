#!/usr/bin/env python
# coding:utf-8

"""
使用ClientDC绘图
"""

import wx

class MainFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "Hello World", 
            size=(800, 600), style=wx.DEFAULT_FRAME_STYLE)

        # 创建面板
        panel = wx.Panel(self, -1)

        # 创建Sizer
        sizer = wx.BoxSizer()

        # 创建用于绘图的面板
        self.palette = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        self.palette.Bind(wx.EVT_MOTION, self.OnMotion)
        sizer.Add(self.palette, 1, wx.EXPAND | wx.ALL ^ wx.RIGHT, 10)

        # 创建演示按钮
        btn = wx.Button(panel, -1, "基本方法")
        btn.Bind(wx.EVT_BUTTON, self.OnBase)
        sizer.Add(btn, 0, wx.ALL, 10)

        # 界面总成
        panel.SetSizer(sizer)
        panel.Layout()

        self.pos = None     # 用于保存鼠标上一次的位置


    def OnBase(self, evt):
        """基本方法按钮点击事件处理"""
                
        # 创建ClientDC
        dc = wx.ClientDC(self.palette)

        dc.Clear()
        
        # 加载图片
        bmp = wx.Bitmap('res/forever.png', wx.BITMAP_TYPE_ANY)

        # 绘制Bitmap
        dc.DrawBitmap(bmp, 100, 50)

        # 设置画笔和画刷
        dc.SetPen(wx.Pen(wx.Colour(224,0,0), 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        w, h = self.palette.GetSize()        
        dc.DrawRectangle(10,10,w-22,h-22)       # 画矩形        
        dc.DrawLine(10,h/2,w-12,h/2)            # 画线

        dc.SetTextForeground(wx.GREEN)
        dc.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Comic Sans MS'))
        dc.DrawText(u'霜重闲愁起', 100, 500)
        dc.DrawRotatedText(u'春深风也疾', 250, 500, 30)

    def OnMotion(self, evt):
        """鼠标移动事件处理"""

        # 判断鼠标左键的状态
        if evt.LeftIsDown():
            # 判断是否保存了上一次的位置
            if self.pos:
                # 创建ClientDC
                dc = wx.ClientDC(self.palette)

                # 设置画笔
                dc.SetPen(wx.Pen(wx.Colour(224,0,0), 1))

                # 画线
                dc.DrawLine(self.pos[0], self.pos[1], evt.x, evt.y) 
            
            # 保存本次位置
            self.pos = (evt.x, evt.y)
        else:
            # 清空保存的位置
            self.pos = None


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
