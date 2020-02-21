#!/usr/bin/env python
# coding:utf-8

"""
wxPython桌面程序模板
"""

import os
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

        # 创建文本框
        self.tc = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.tc.Enable(False)
        self.tc.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        self.file = ""        

        # 创建菜单栏
        self.CreateMenuBar()

        # 创建工具栏
        self.CreateToolBar()

        # 创建状态栏
        self.CreateStatusBar()

    def CreateMenuBar(self):
        """创建菜单栏"""

        # 创建菜单栏
        mb = wx.MenuBar()

        # 创建菜单
        fileMenu = wx.Menu()

        # 向菜单中加入菜单项
        item = fileMenu.Append(wx.ID_OPEN, "打开(&O)", "选择并打开txt文件")

        exit_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_MENU, (16, 16))
        fileMenu.Append(wx.ID_SAVE, "保存(&S)", "将修改的内容保存到txt文件中")

        # 向菜单中加入分隔条
        fileMenu.AppendSeparator()

        # 另一种创建菜单项的方式
        exit = wx.MenuItem(fileMenu, wx.ID_EXIT, "退出(&E)", "退出文件编辑器")
        exit_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU, (16, 16))
        exit.SetBitmap(exit_bmp)
        fileMenu.Append(exit)

        # 将菜单加入菜单栏
        mb.Append(fileMenu, "文件(&F)")

        # 创建设置菜单
        config = wx.Menu()

        # 嵌套菜单
        theme = wx.Menu()
        
        bw = wx.MenuItem(theme, wx.NewIdRef(), "黑底白字(&B)", "设置显示主题为黑底白字", kind=wx.ITEM_RADIO)
        theme.Append(bw)
        wb = wx.MenuItem(theme, wx.NewIdRef(), "白底黑字(&B)", "设置显示主题为白底黑字", kind=wx.ITEM_RADIO)
        theme.Append(wb)

        config.Append(wx.NewIdRef(), "主题(&T)", theme)

        option = wx.Menu()        
        option.Append(wx.NewIdRef(), "自动保存(&A)", "设置是否开启自动保存", kind=wx.ITEM_CHECK)
        config.AppendSubMenu(option, "首选项(&O)")

        mb.Append(config, "设置(&C)")

        # 为窗口设置菜单栏
        self.SetMenuBar(mb)

        # 绑定事件
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

    def CreateToolBar(self):
        """创建工具栏"""

        # 创建工具栏
        tb = wx.ToolBar(self, style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

        # 设置图标大小
        tsize = (24, 24)
        tb.SetToolBitmapSize(tsize)

        # 添加普通工具
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        tb.AddTool(wx.ID_OPEN, "打开", open_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "打开", "选择并打开txt文件")

        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        tb.AddTool(wx.ID_SAVE, "保存", save_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "保存", "将修改的内容保存到txt文件中")

        # 添加分隔条
        tb.AddSeparator()

        # 添加单选工具
        bw_bmp = wx.Bitmap(os.path.join("res", "bw.png"))
        tb.AddTool(wx.NewIdRef(), "黑底白字", bw_bmp, wx.NullBitmap, wx.ITEM_RADIO, "黑底白字", "设置显示主题为黑底白字")

        wb_bmp = wx.Bitmap(os.path.join("res", "wb.png"))
        tb.AddTool(wx.NewIdRef(), "白底黑字", wb_bmp, wx.NullBitmap, wx.ITEM_RADIO, "白底黑字", "设置显示主题为白底黑字")

        # 添加勾选工具
        autosave_bmp = wx.Bitmap(os.path.join("res", "autosave.png"))
        tb.AddTool(wx.NewIdRef(), "自动保存", autosave_bmp, wx.NullBitmap, wx.ITEM_CHECK, "自动保存", "设置是否开启自动保存")

        # 添加工具后必须调用
        tb.Realize()

        # 为窗口设置工具栏
        self.SetToolBar(tb)

    def CreateStatusBar(self):
        """创建状态栏"""

        self.sb = wx.StatusBar(self, -1)
        self.sb.SetFieldsCount(2)
        self.sb.SetStatusWidths([-1, -1])

        self.sb.SetStatusText("就绪", 0)
        self.sb.SetStatusText("请先打开文件", 1)

        self.SetStatusBar(self.sb)

    def OnOpen(self, evt):
        """打开文件事件处理"""
        
        dlg = wx.FileDialog(self, "打开文件", wildcard="文本文件|*.txt")

        if dlg.ShowModal() == wx.ID_OK:
            self.file = dlg.GetPath()

            # 加载文件
            self.tc.LoadFile(self.file)
            self.tc.Enable(True)

            # 设置状态栏
            self.sb.SetStatusText(self.file, 1)

    def OnSave(self, evt):
        """保存文件事件处理"""

        self.tc.SaveFile(self.file)

    def OnExit(self, evt):
        """退出事件处理"""

        self.Destroy()

    def OnRightUp(self, evt):
        """弹出菜单"""

        # 创建设置菜单
        config = wx.Menu()

        # 嵌套菜单
        theme = wx.Menu()
        
        bw = wx.MenuItem(theme, wx.NewIdRef(), "黑底白字(&B)", kind=wx.ITEM_RADIO)
        theme.Append(bw)
        wb = wx.MenuItem(theme, wx.NewIdRef(), "白底黑字(&B)", kind=wx.ITEM_RADIO)
        theme.Append(wb)

        config.Append(wx.NewIdRef(), "主题(&T)", theme)

        option = wx.Menu()        
        option.Append(wx.NewIdRef(), "自动保存(&A)", kind=wx.ITEM_CHECK)
        config.Append(wx.NewIdRef(), "首选项(&O)", option)

        self.PopupMenu(config)

    

class MainApp(wx.App):
    """主应用程序"""

    def OnInit(self):
        """主应用程序初始化回调函数"""

        self.SetAppName(APP_TITLE)
        self.frame = MainFrame(None)
        self.frame.Show()

        return True

    def GetMainFrame():
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