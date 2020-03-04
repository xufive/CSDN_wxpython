#!/usr/bin/env python
# coding:utf-8

import os
import wx
import wx.adv
import imageio
import win32con
import datetime
import threading
import configparser
from PIL import ImageGrab
import wx.lib.filebrowsebutton as filebrowse


class MainFrame(wx.Frame):
    MENU_START  = wx.NewIdRef()      # 开始录制
    MENU_STOP   = wx.NewIdRef()      # 停止录制
    MENU_CONFIG = wx.NewIdRef()      # 设置
    MENU_FOLFER = wx.NewIdRef()      # 打开输出目录
    MENU_EXIT   = wx.NewIdRef()      # 退出

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "", size=(800, 600),
                          style=wx.FRAME_SHAPED | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        # 启用双缓冲
        self.SetDoubleBuffered(True)

        # 初始化变量
        self.topLeft   = None     # 左上锚点
        self.top       = None     # 上锚点
        self.topRight  = None     # 右上锚点
        self.left      = None     # 左锚点
        self.right     = None     # 右锚点
        self.btmLeft   = None     # 左下锚点
        self.btm       = None     # 下锚点
        self.btmRight  = None     # 右下锚点
        self.recording = False    # 是否正在录制
        self.saveing   = False    # 是否正在生成GIF
        self.startTime = None     # 录制开始时间
        self.endTime   = None     # 录制结束时间
        self.imgs      = []       # 每帧的图片列表

        # 读取配置项
        self.config = self.ReadConfig()

        # 添加系统托盘
        icon = wx.Icon(os.path.join("res", "recorder.ico"), wx.BITMAP_TYPE_ICO)
        self.taskBar = wx.adv.TaskBarIcon()
        self.taskBar.SetIcon(icon, "屏幕录像机")

        # 注册热键
        self.RegisterHotKey(self.MENU_START, win32con.MOD_CONTROL, win32con.VK_F2)
        self.RegisterHotKey(self.MENU_STOP, win32con.MOD_SHIFT, win32con.VK_F2)

        # 设置不规则窗口
        self.SetWindowShape()

        # 居中
        self.CenterOnScreen()

        # 创建录像定时器
        self.timer = wx.Timer(self)  # 创建定时器

        # 绑定事件
        self.Bind(wx.EVT_MOTION, self.OnMotion)             # 鼠标移动
        self.Bind(wx.EVT_PAINT, self.OnPaint)               # 窗口重绘
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBG)  # 擦除背景
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)   # 定时器

        self.taskBar.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnTaskBar)       # 右键单击托盘图标
        self.taskBar.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnTaskBar)        # 左键单击托盘图标
        self.taskBar.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBar)    # 左键双击托盘图标

        self.taskBar.Bind(wx.EVT_MENU, self.OnStart, id=self.MENU_START)        # 开始录制
        self.taskBar.Bind(wx.EVT_MENU, self.OnStop, id=self.MENU_STOP)            # 停止录制
        self.taskBar.Bind(wx.EVT_MENU, self.OnOpenFolder, id=self.MENU_FOLFER)  # 打开输出目录
        self.taskBar.Bind(wx.EVT_MENU, self.OnConfig, id=self.MENU_CONFIG)      # 设置
        self.taskBar.Bind(wx.EVT_MENU, self.OnExit, id=self.MENU_EXIT)          # 退出

        self.Bind(wx.EVT_HOTKEY, self.OnStart, id=self.MENU_START)              # 开始录制热键
        self.Bind(wx.EVT_HOTKEY, self.OnStop, id=self.MENU_STOP)                  # 停止录制热键

    def ReadConfig(self):
        """读取配置文件"""

        config = configparser.ConfigParser()

        if os.path.isfile("recorder.ini"):
            config.read("recorder.ini")
        else:
            config.read_dict({
                "recoder": {
                    "fps": 10,
                    "loop": 0,
                    "outdir": "d:\\"
                }
            })
            config.write(open("recorder.ini", "w"))

        return config

    def SetWindowShape(self):
        """设置窗口形状"""

        # 计算窗口形状
        w, h = self.GetSize()

        path = wx.GraphicsRenderer.GetDefaultRenderer().CreatePath()

        # 左上角
        self.topLeft = (0, 0, 10, 10)
        path.AddRectangle(self.topLeft[0], self.topLeft[1], self.topLeft[2], self.topLeft[3])

        # 上边线
        path.AddRectangle(10, 5, (w/2)-15, 5)

        self.top = ((w/2)-5, 0, 10, 10)
        path.AddRectangle(self.top[0], self.top[1], self.top[2], self.top[3])

        path.AddRectangle((w/2)+5, 5, (w/2)-15, 5)

        # 右上角
        self.topRight = (w - 10, 0, 10, 10)
        path.AddRectangle(self.topRight[0], self.topRight[1], self.topRight[2], self.topRight[3])

        # 右边线
        path.AddRectangle(w-10, 10, 5, (h/2)-15)

        self.right = (w-10, (h/2)-5, 10, 10)
        path.AddRectangle(self.right[0], self.right[1], self.right[2], self.right[3])

        path.AddRectangle(w-10, (h/2)+5, 5, (h/2)-15)

        # 右下角
        self.btmRight = (w-10, h-10, 10, 10)
        path.AddRectangle(self.btmRight[0], self.btmRight[1], self.btmRight[2], self.btmRight[3])

        # 下边线
        path.AddRectangle((w/2)+5, h-10, (w/2)-15, 5)

        self.btm = ((w/2)-5, h-10, 10, 10)
        path.AddRectangle(self.btm[0], self.btm[1], self.btm[2], self.btm[3])

        path.AddRectangle(10, h-10, (w/2)-15, 5)

        # 左下角
        self.btmLeft = (0, h - 10, 10, 10)
        path.AddRectangle(self.btmLeft[0], self.btmLeft[1], self.btmLeft[2], self.btmLeft[3])

        # 左边线
        path.AddRectangle(5, (h/2)+5, 5, (h/2)-15)

        self.left = (0, (h/2)-5, 10, 10)
        path.AddRectangle(self.left[0], self.left[1], self.left[2], self.left[3])

        path.AddRectangle(5, 10, 5, (h/2)-15)

        # 设计窗口形状
        self.SetShape(path)

    def OnPaint(self, evt):
        """窗口重绘事件处理"""

        # 绘制DC
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.RED_BRUSH if self.recording else wx.GREEN_BRUSH)
        w, h = self.GetSize()
        dc.DrawRectangle(0, 0, w, h)

    def OnEraseBG(self, evt):
        """擦除背景事件处理"""

        pass

    def OnMotion(self, evt):
        """鼠标移动事件处理"""

        # 鼠标相对于窗口的位置
        x = evt.x
        y = evt.y

        # 鼠标相对于屏幕的位置
        sx, sy = self.ClientToScreen(x, y)

        # 窗口相对于屏幕的位置
        px, py = self.GetPosition()

        # 窗口大小
        w, h = self.GetSize()

        # 屏幕大小
        sw, sh = wx.DisplaySize()

        # 在左上角锚点内
        if self.topLeft[0] < x < self.topLeft[0]+self.topLeft[2] \
                and self.topLeft[1] < y < self.topLeft[1]+self.topLeft[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENWSE))
            if evt.LeftIsDown():
                npx = sx - 5 if sx-5 > 0 else 0
                npy = sy - 5 if sy - 5 > 0 else 0
                self.SetPosition((npx, npy))
                self.SetSize((w-(npx-px), h-(npy-py)))

        # 在上锚点内
        if self.top[0] < x < self.top[0]+self.top[2] \
                and self.top[1] < y < self.top[1]+self.top[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))
            if evt.LeftIsDown():
                npy = sy - 5 if sy - 5 > 0 else 0
                self.SetPosition((px, npy))
                self.SetSize((w, h-(npy-py)))

        # 在右上锚点内
        if self.topRight[0] < x < self.topRight[0] + self.topRight[2] \
                and self.topRight[1] < y < self.topRight[1] + self.topRight[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENESW))
            if evt.LeftIsDown():
                if sx + 5 < sw:
                    sx += 5

                npy = sy - 5 if sy - 5 > 0 else 0
                self.SetPosition((px, npy))
                self.SetSize((sx-px, h - (npy - py)))

        # 在右锚点内
        if self.right[0] < x < self.right[0] + self.right[2] \
                and self.right[1] < y < self.right[1] + self.right[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZEWE))
            if evt.LeftIsDown():
                if sx + 5 < sw:
                    sx += 5
                self.SetSize((sx - px, h))

        # 在右下锚点内
        if self.btmRight[0] < x < self.btmRight[0] + self.btmRight[2] \
                and self.btmRight[1] < y < self.btmRight[1] + self.btmRight[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENWSE))
            if evt.LeftIsDown():
                if sx + 5 < sw:
                    sx += 5
                if sy + 5 < sh:
                    sy += 5
                self.SetSize((sx-px, sy-py))

        # 在下锚点内
        if self.btm[0] < x < self.btm[0] + self.btm[2] \
                and self.btm[1] < y < self.btm[1] + self.btm[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))
            if evt.LeftIsDown():
                if sy + 5 < sh:
                    sy += 5
                self.SetSize((w, sy-py))

        # 在左下锚点内
        if self.btmLeft[0] < x < self.btmLeft[0] + self.btmLeft[2] \
                and self.btmLeft[1] < y < self.btmLeft[1] + self.btmLeft[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENESW))
            if evt.LeftIsDown():
                if sy + 5 < sh:
                    sy += 5

                npx = sx - 5 if sx - 5 > 0 else 0
                self.SetPosition((npx, py))
                self.SetSize((w-(npx-px), sy))

        # 在左锚点内
        if self.left[0] < x < self.left[0] + self.left[2] \
                and self.left[1] < y < self.left[1] + self.left[3]:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZEWE))
            if evt.LeftIsDown():
                npx = sx - 5 if sx - 5 > 0 else 0
                self.SetPosition((npx, py))
                self.SetSize((w-(npx-px), h))

        self.SetWindowShape()

    def OnTaskBar(self, evt):
        """托盘图标操作事件处理"""

        # 创建菜单
        menu = wx.Menu()
        menu.Append(self.MENU_START, "开始录制(Ctrl+F2)")
        menu.Append(self.MENU_STOP, "停止录制(Shift+F2)")
        menu.AppendSeparator()
        menu.Append(self.MENU_FOLFER, "打开输出目录")
        menu.Append(self.MENU_CONFIG, "设置")
        menu.AppendSeparator()
        menu.Append(self.MENU_EXIT, "退出")

        # 设置状态
        if self.recording:
            menu.Enable(self.MENU_START, False)
            menu.Enable(self.MENU_STOP, True)
            menu.Enable(self.MENU_CONFIG, False)
        else:
            menu.Enable(self.MENU_START, True)
            menu.Enable(self.MENU_STOP, False)
            menu.Enable(self.MENU_CONFIG, True)

        self.taskBar.PopupMenu(menu)
        menu.Destroy()

    def OnTimer(self, evt):
        """定时器事件处理"""

        # 计算坐标
        left = self.left[0] + self.left[2]
        top = self.top[1] + self.top[3]
        right = self.right[0] - 1
        bottom = self.btm[1] - 1

        left, top = self.ClientToScreen(left, top)
        right, bottom = self.ClientToScreen(right, bottom)

        # 截图
        img = ImageGrab.grab((left, top, right, bottom))
        self.imgs.append(img)

        if len(self.imgs) >= 200:
            self.OnStop(None)

    def OnStart(self, evt):
        """开始录制菜单事件处理"""

        self.startTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.recording = True

        # 启动定时器
        self.timer.Start(1000/self.config.getint("recoder", "fps"))

        # 刷新窗口
        self.Refresh()

    def OnStop(self, evt):
        """停止录制菜单事件处理"""

        # 停止定时器
        self.timer.Stop()

        self.endTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.recording = False

        # 刷新窗口
        self.Refresh()

        # 启动生成GIF线程
        t = threading.Thread(target=self.CreateGif)
        t.setDaemon(True)
        t.start()

        # 启动等待线程
        t = threading.Thread(target=self.Waiting)
        t.setDaemon(True)
        t.start()

    def Waiting(self):
        """显示等待对话框"""

        dlg = wx.ProgressDialog("生成GIF",
                                "正在渲染，请稍候",
                                parent=self,
                                style=wx.PD_APP_MODAL
                                      | wx.PD_ELAPSED_TIME
                                      | wx.PD_ESTIMATED_TIME
                                      | wx.PD_REMAINING_TIME
                                )
        self.saveing = True
        while True:
            if self.saveing:
                dlg.Pulse()
                wx.MilliSleep(100)
            else:
                dlg.Destroy()
                break

    def CreateGif(self):
        """生成gif动画线程"""

        # 生成GIF
        filePath = os.path.join(self.config.get("recoder", "outdir"),
                                "%s-%s.gif" % (self.startTime, self.endTime))
        fps = self.config.getint("recoder", "fps")
        loop = self.config.getboolean("recoder", "loop")
        imageio.mimsave(filePath, self.imgs, fps=fps, loop=loop)

        self.saveing = False

    def OnOpenFolder(self, evt):
        """打开输出目录"""

        outdir = self.config.get("recoder", "outdir")
        os.system("explorer %s" % outdir)

    def OnConfig(self, evt):
        """设置菜单事件处理"""

        # 创建设置对话框
        dlg = ConfigDlg(self,
                        self.config.getint("recoder", "fps"),
                        self.config.getboolean("recoder", "loop"),
                        self.config.get("recoder", "outdir")
                        )

        # 以模态方式显示对话框
        if dlg.ShowModal() == wx.ID_OK:
            # 保存设置
            self.config.set("recoder", "fps", str(dlg.GetFps()))
            self.config.set("recoder", "loop", "1" if dlg.GetLoop() else "0")
            self.config.set("recoder", "outdir", dlg.GetOutDir())
            self.config.write(open("recorder.ini", "w"))

        # 销毁设置对话框
        dlg.Destroy()

    def OnExit(self, evt):
        """退出菜单事件处理"""

        # 从托盘删除图标
        self.taskBar.RemoveIcon()

        # 退出
        wx.Exit()


class ConfigDlg(wx.Dialog):
    """
    设置窗口
    """

    def __init__(self, parent, fps, loop, outdir):
        """
        ConfigDlg的构造函数
        """

        wx.Dialog.__init__(self, parent, -1, "设置", size=(450, 200))

        # 创建布局管理器
        sizer = wx.BoxSizer()
        grid = wx.GridBagSizer(10, 10)

        # 帧率
        text = wx.StaticText(self, -1, "帧率")
        grid.Add(text, (0, 0), flag=wx.TOP | wx.ALIGN_RIGHT, border=5)

        self.fps = wx.SpinCtrl(self, -1)
        self.fps.SetValue(fps)
        grid.Add(self.fps, (0, 1), flag=wx.EXPAND | wx.LEFT, border=10)

        # 是否循环
        self.loop = wx.CheckBox(self, -1, "是否循环")
        self.loop.SetValue(loop)
        grid.Add(self.loop, (0, 2), flag=wx.EXPAND)

        # 输出路径
        text = wx.StaticText(self, -1, "输出目录")
        grid.Add(text, (1, 0), flag=wx.TOP, border=10)
        self.outdir = filebrowse.DirBrowseButton(self, -1, labelText="", buttonText="浏览", toolTip="请选择输出路径")
        self.outdir.SetValue(outdir)
        grid.Add(self.outdir, (1, 1), (1, 2), flag=wx.EXPAND)

        # 按钮，直接使用内置的ID，可以省略事件处理函数，使用wxPython内置的事件处理
        subgrid = wx.GridBagSizer(10, 10)
        okBtn = wx.Button(self, wx.ID_OK, "确定")
        subgrid.Add(okBtn, (0, 0), flag=wx.ALIGN_RIGHT)

        canelBtn = wx.Button(self, wx.ID_CANCEL, "取消")
        subgrid.Add(canelBtn, (0, 1))
        grid.Add(subgrid, (2, 0), (1, 3), flag=wx.ALIGN_CENTER)

        # 界面总成
        grid.AddGrowableCol(2)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(sizer)
        self.Layout()

        self.CenterOnScreen()

    def GetFps(self):
        """取得频率设置"""

        return self.fps.GetValue()

    def GetLoop(self):
        """取得循环设置"""

        return self.loop.GetValue()

    def GetOutDir(self):
        """取得输入目录设置"""

        return self.outdir.GetValue()

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
