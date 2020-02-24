#-*- coding: utf-8 -*-

import wx
import sys, os, time
import threading

APP_TITLE = u'定时器和线程'
APP_ICON = 'res/wx.ico'

class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''
    
    def __init__(self, parent):
        '''构造函数'''
        
        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224)) # 设置窗口背景色
        self.SetSize((320, 300)) # 设置窗口大小
        self.Center() # 设置窗口居中
        
        icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon) # 设置窗口图标
        
        font = wx.Font(30, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Monaco') # 定义字体字号
        
        self.clock = wx.StaticText(self, -1, u'08:00:00', pos=(50,50), size=(200,50), style=wx.TE_CENTER|wx.SUNKEN_BORDER)
        self.clock.SetBackgroundColour(wx.Colour(0, 0, 0)) # 设置时钟背景色
        self.clock.SetForegroundColour(wx.Colour(0, 224, 32)) # 设置时钟前景色
        self.clock.SetFont(font) # 设置时钟字体字号
        
        self.stopwatch = wx.StaticText(self, -1, u'0:00:00.0', pos=(50,150), size=(200,50), style=wx.TE_CENTER|wx.SUNKEN_BORDER)
        self.stopwatch.SetBackgroundColour(wx.Colour(0, 0, 0)) # 设置秒表背景色
        self.stopwatch.SetForegroundColour(wx.Colour(0, 224, 32)) # 设置秒表前景色
        self.stopwatch.SetFont(font) # 设置秒表字体字号
        
        self.timer = wx.Timer(self) # 创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer) # 绑定定时器事件
        self.timer.Start(100, oneShot=False) # 启动定时器，间隔100ms；若oneShot为真，则只启动一次
        
        self.is_start = False # 秒表是否启动
        self.t_start = None # 秒表启动时间
        
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown) # 绑定键盘事件
        
        thread_sw = threading.Thread(target=self.StopWatchThread)
        thread_sw.setDaemon(True)
        thread_sw.start()
        
    def OnTimer(self, evt):
        '''定时器函数'''
        
        t = time.localtime()
        self.clock.SetLabel('%02d:%02d:%02d'%(t.tm_hour, t.tm_min, t.tm_sec))
        
    def OnKeyDown(self, evt):
        '''键盘事件函数'''
        
        if evt.GetKeyCode() == wx.WXK_SPACE:
            self.is_start = not self.is_start
            self.t_start= time.time()
        elif evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.is_start = False
            self.stopwatch.SetLabel('0:00:00.0')
        
    def StopWatchThread(self):
        '''线程函数'''
        
        while True:
            if self.is_start:
                n = int(10*(time.time() - self.t_start))
                deci = n%10
                ss = int(n/10)%60
                mm = int(n/600)%60
                hh = int(n/36000)
                wx.CallAfter(self.stopwatch.SetLabel, '%d:%02d:%02d.%d'%(hh, mm, ss, deci))
            time.sleep(0.02)
        
class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show()
        return True

if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()