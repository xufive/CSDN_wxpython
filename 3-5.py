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
        panel.SetDoubleBuffered(True)

        # 创建Sizer
        sizer = wx.BoxSizer()

        # 创建用于绘图的面板
        self.palette = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        self.palette.Bind(wx.EVT_MOTION, self.OnMotion)
        self.palette.Bind(wx.EVT_PAINT, self.OnPaint)
        self.palette.Bind(wx.EVT_SIZE, self.OnSize)
        sizer.Add(self.palette, 1, wx.EXPAND | wx.ALL ^ wx.RIGHT, 10)

        # 创建演示按钮
        btn = wx.Button(panel, -1, "基本方法")
        btn.Bind(wx.EVT_BUTTON, self.OnBase)
        sizer.Add(btn, 0, wx.ALL, 10)

        # 界面总成
        panel.SetSizer(sizer)
        panel.Layout()

        # 使用变量记录绘图数据
        self.pw = 0         # 面板原始宽度
        self.ph = 0         # 面板原始高度
        self.wr = 1         # 宽度缩放比率
        self.hr = 1         # 高度缩放比率
        self.bmp = None     # 图片
        self.zoomw = 1      # 窗口宽度缩放比率
        self.zoomh = 1      # 窗口高度缩放比率
        self.pos = None     # 鼠标上一次的位置
        self.lines = []     # 鼠标画的轨迹线        
        self.texts = []      # 文本信息：(文本内容, x, y, 旋转角度)


    def OnBase(self, evt):
        """基本方法按钮点击事件处理"""

        self.pw, self.ph = self.palette.GetSize()
        
        # 加载图片
        self.bmp = wx.Bitmap('res/forever.png', wx.BITMAP_TYPE_ANY)

        # 设置文本数据
        self.texts.append(("霜重闲愁起", 100, 500, 0))
        self.texts.append(("春深风也疾", 250, 500, 30))

        # 触发重绘
        self.palette.Refresh()

    def OnMotion(self, evt):
        """鼠标移动事件处理"""

        # 判断鼠标左键的状态
        if evt.LeftIsDown():
            # 判断是否保存了上一次的位置
            if self.pos:
                self.lines.append((self.pos[0], self.pos[1], evt.x/self.wr, evt.y/self.hr))
            
            # 保存本次位置
            self.pos = (evt.x/self.wr, evt.y/self.wr)
        else:
            # 清空保存的位置
            self.pos = None

        # 触发重绘
        self.palette.Refresh()

    def OnSize(self, evt):
        """窗口大小变化事件处理"""

        if hasattr(self, "pw") and self.pw > 0:
            # 计算缩放比率
            pw, ph = self.palette.GetSize() 
            self.wr = pw / self.pw
            self.hr = ph / self.ph

            # 触发窗口重绘
            self.palette.Refresh()

    def OnPaint(self, evt):
        """重绘事件处理"""

        # 创建PaintDC
        dc = wx.PaintDC(self.palette)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.Colour(224,0,0), 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)        

        # 绘制图片
        if self.bmp:
            # 计算图片位置
            pw, ph = self.palette.GetSize()       
            bw, wh = self.bmp.GetSize()
            w = (pw - bw) / 2
            h = (ph - wh) / 2

            dc.DrawBitmap(self.bmp, w, h)
            dc.DrawRectangle(10, 10, pw-22, ph-22)
            dc.DrawLine(10, ph/2, pw-12, ph/2)        

        # 画鼠标轨迹
        for line in self.lines:
            dc.DrawLine(line[0]*self.wr, line[1]*self.hr, line[2]*self.wr, line[3]*self.hr)

        # 画文本
        for text in self.texts:
            dc.DrawRotatedText(text[0], (text[1]*self.wr, text[2]*self.hr), text[3])
            

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
