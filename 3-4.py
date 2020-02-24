#-*- coding: utf-8 -*-

import wx
import os

APP_TITLE = u'使用DC绘图'
APP_ICON = 'res/wx.ico'

class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''
    
    def __init__(self, parent):
        '''构造函数'''
        
        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.Center()
        
        icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        self.palette = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        self.palette.SetBackgroundColour(wx.Colour(0, 0, 0))
        btn_base = wx.Button(self, -1, u'基本方法', size=(100, -1))
        
        sizer_max = wx.BoxSizer()
        sizer_max.Add(self.palette, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        sizer_max.Add(btn_base, 0, wx.ALL, 20)
        
        self.SetAutoLayout(True)
        self.SetSizer(sizer_max)
        self.Layout()
        
        btn_base.Bind(wx.EVT_BUTTON, self.OnBase)
        self.palette.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.palette.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.xy = None # 鼠标画线的起点
        self.lines = list() # 保存鼠标化的线
        self.img = wx.Bitmap('res/forever.png', wx.BITMAP_TYPE_ANY)
        
    def OnMouse(self, evt):
        '''移动鼠标画线'''
        
        if evt.EventType == wx.EVT_LEFT_DOWN.evtType[0]: #左键按下
            self.xy = (evt.x, evt.y)
        elif evt.EventType == wx.EVT_LEFT_UP.evtType[0]: #左键弹起
            self.xy = None
        elif evt.EventType == wx.EVT_MOTION.evtType[0]: #鼠标移动
            if self.xy:
                dc = wx.ClientDC(self.palette)
                dc.SetPen(wx.Pen(wx.Colour(0,224,0), 2))
                dc.DrawLine(self.xy[0], self.xy[1], evt.x, evt.y)
                self.lines.append((self.xy[0], self.xy[1], evt.x, evt.y))
                self.xy = (evt.x, evt.y)
        
    def OnBase(self, evt):
        '''DC基本方法演示'''
        
        w, h = self.palette.GetSize()
        
        dc = wx.ClientDC(self.palette) # 创建DC
        dc.SetBrush(wx.Brush(wx.Colour(0,80,80) )) # 设置画刷
        dc.SetPen(wx.Pen(wx.Colour(224,0,0), 1)) # 设置画笔
        dc.DrawRectangle(10,10,w-22,h-22) # 画矩形
        
        dc.SetPen(wx.Pen(wx.Colour(0,224,224), 1)) # 设置画笔
        dc.DrawLine(10,h/2,w-12,h/2) # 画线
        
        dc.DrawBitmap(self.img, 80, 30) # 画位图
        
        dc.SetTextForeground(wx.Colour(224,224,224)) # 设置文本颜色
        dc.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Comic Sans MS'))
        dc.DrawText(u'霜重闲愁起', 100, 500)
        dc.DrawRotatedText(u'春深风也疾', 250, 500, 30)
        
    def OnPaint(self, evt):
        '''重绘事件函数'''
        
        w, h = self.palette.GetSize()
        dc = wx.PaintDC(self.palette)
        
        dc.SetBrush(wx.Brush(wx.Colour(0,80,80) ))
        dc.SetPen(wx.Pen(wx.Colour(224,0,0), 1))
        dc.DrawRectangle(10,10,w-22,h-22)
        
        dc.SetPen(wx.Pen(wx.Colour(0,224,224), 1))
        dc.DrawLine(10,h/2,w-12,h/2)
        
        dc.DrawBitmap(self.img, 80, 30)
        
        dc.SetTextForeground(wx.Colour(224,224,224))
        dc.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Comic Sans MS'))
        dc.DrawText(u'霜重闲愁起', 100, 500)
        dc.DrawRotatedText(u'春深风也疾', 250, 500, 30)
        
        dc.SetPen(wx.Pen(wx.Colour(0,224,0), 2))
        for line in self.lines:
            dc.DrawLine(line[0],line[1],line[2],line[3])
    
class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show()
        return True

if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
