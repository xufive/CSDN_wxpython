#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用wxPython制作简易的Python代码编辑器
"""

import os
import wx
import keyword
import wx.py as py
import wx.stc as stc
import wx.lib.agw.aui as aui

APP_TITLE = "PyEditor"


# ================================================================================
class MainFrame(wx.Frame):
    """主窗口"""

    # --------------------------------------------------------------------------------
    def __init__(self, parent=None):
        """构造函数"""

        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.Maximize()

        # 设置图标
        icon = wx.Icon(os.path.join("res", "PyEditor.ico"))
        self.SetIcon(icon)

        # 主框架布局
        self._mgr = aui.AuiManager()

        # 生成菜单栏
        self.__CreateMenuBar()

        # 生成工具栏
        self.__CreateToolbar()

        # 生成状态栏
        self.__CreateStatusbar()

        # 生成代码编辑区
        self.__CreateEditorView()

        # 生成目录树
        self.__CreateTreeView()

        # 生成信息区
        self.__CreateDebugView()

        # 总成
        self._mgr.SetManagedWindow(self)
        self._mgr.Update()

        # 绑定事件
        self.__BindEvt()

    # --------------------------------------------------------------------------------
    def __CreateMenuBar(self):
        """生成菜单栏"""

        msize = (16, 16)        # 图片大小

        self.mb = wx.MenuBar()

        # 创建文件菜单
        fileMenu = wx.Menu()

        # 打开工程菜单项
        openFolder = wx.MenuItem(fileMenu, wx.ID_OPEN, "打开工程(&O)", "打开工程文件夹")
        openBmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_MENU, msize)
        openFolder.SetBitmap(openBmp)
        fileMenu.Append(openFolder)

        # 保存菜单项
        saveFile = wx.MenuItem(fileMenu, wx.ID_SAVE, "保存文件(&S)", "将修改保存到文件中")
        saveBmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, msize)
        saveFile.SetBitmap(saveBmp)
        fileMenu.Append(saveFile)

        # 分隔条
        fileMenu.AppendSeparator()

        # 退出菜单项
        exit = wx.MenuItem(fileMenu, wx.ID_EXIT, "退出(&E)", "退出Python代码编辑器")
        exitBmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU, msize)
        exit.SetBitmap(exitBmp)
        fileMenu.Append(exit)

        self.mb.Append(fileMenu, "文件(&F)")

        # 编辑菜单
        editMenu = wx.Menu()

        # 撤销菜单项
        undo = wx.MenuItem(editMenu, wx.ID_UNDO, "撤销(&R)", "撤销上一次修改")
        undoBmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_MENU, msize)
        undo.SetBitmap(undoBmp)
        editMenu.Append(undo)

        # 重做菜单项
        redo = wx.MenuItem(editMenu, wx.ID_REDO, "重做(&U)", "重做撤销的修改")
        redoBmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_MENU, msize)
        redo.SetBitmap(redoBmp)
        editMenu.Append(redo)

        self.mb.Append(editMenu, "编辑(&E)")

        self.SetMenuBar(self.mb)

    # --------------------------------------------------------------------------------
    def __CreateToolbar(self):
        """生成工具栏"""

        # 创建AuiToolBar
        self.tb = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                                 agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)

        # 图标大小
        tsize = wx.Size(24, 24)
        self.tb.SetToolBitmapSize(tsize)

        # 打开目录
        self.tb.AddTool(wx.ID_OPEN, "打开目录",
                        wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_TOOLBAR, tsize),
                        wx.NullBitmap, wx.ITEM_NORMAL, "打开目录", "打开工程文件夹")

        # 保存文件
        self.tb.AddTool(wx.ID_SAVE, "保存文件",
                        wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize),
                        wx.NullBitmap, wx.ITEM_NORMAL, "保存文件", "将修改保存到文件中")

        # 分隔条
        self.tb.AddSeparator()

        # 撤销
        self.tb.AddTool(wx.ID_UNDO, "撤销",
                        wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, tsize),
                        wx.NullBitmap, wx.ITEM_NORMAL, "撤销", "撤销上一次修改")

        # 重做
        self.tb.AddTool(wx.ID_REDO, "重做",
                        wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, tsize),
                        wx.NullBitmap, wx.ITEM_NORMAL, "重做", "重做撤销的修改")

        self.tb.Realize()
        self._mgr.AddPane(self.tb, aui.AuiPaneInfo().Name("toolbar").Caption("Big Toolbar").
                          ToolbarPane().Top())

    def __CreateStatusbar(self):
        """创建状态栏"""

        self.sb = wx.StatusBar(self, -1)
        self.sb.SetFieldsCount(2)
        self.sb.SetStatusWidths([-1, -1])

        self.sb.SetStatusText("就绪", 0)
        self.sb.SetStatusText("请先打开文件", 1)

        self.SetStatusBar(self.sb)

    # --------------------------------------------------------------------------------
    def __CreateTreeView(self):
        """生成目录树窗口"""

        self.tree = ProjectTree(self)

        self._mgr.AddPane(self.tree, aui.AuiPaneInfo().Name("tree view").Caption("目录树").
                          Left().Layer(1).Position(1).MinSize((300, -1)).CloseButton(True).MinimizeButton(True))

    # --------------------------------------------------------------------------------
    def __CreateEditorView(self):
        """生成代码编辑区"""

        # 创建auiNotebook
        self.nb = aui.AuiNotebook(self, -1)

        # 添加欢迎页
        panel = wx.Panel(self.nb, -1)
        sizer = wx.BoxSizer()
        bmp = wx.StaticBitmap(panel, -1, wx.Bitmap(os.path.join("res", "PyEditor.png")))
        sizer.Add(bmp, 1, flag=wx.ALIGN_CENTER)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        self.nb.AddPage(panel, "欢迎")

        self._mgr.AddPane(self.nb, aui.AuiPaneInfo().Name("code edit").
                          CenterPane().PaneBorder(False))

    # --------------------------------------------------------------------------------
    def __CreateDebugView(self):
        """生成调试区"""

        crust = py.crust.Crust(self, -1)
        self._mgr.AddPane(crust, aui.AuiPaneInfo().Name("debug view").Caption("调试").
                          Bottom().Layer(1).Position(1).MinSize((-1, 200)).MinimizeButton(True).MaximizeButton(True))

    def __BindEvt(self):
        """绑定事件"""

        self.Bind(wx.EVT_MENU, self.OpenProject, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.SaveFile, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.UnDo, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, self.ReDo, id=wx.ID_REDO)


    # --------------------------------------------------------------------------------
    def OpenProject(self, evt=None):
        """打开工程"""

        dlg = wx.DirDialog(self, "请选择工程路径", style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetProjectPath(dlg.GetPath())
        dlg.Destroy()

    def OpenFile(self, filePath):
        """打开文件"""

        pstc = PythonSTC(self.nb, -1, filePath)
        fileName = os.path.basename(filePath)
        
        page = self.nb.AddPage(pstc, "fileName")
        self.nb.SetSelection(page)

        # 设置状态栏
        self.sb.SetStatusText(filePath, 1)

    # --------------------------------------------------------------------------------
    def SaveFile(self, evt):
        """保存文件"""

        self.nb.GetCurrentPage().SaveFile()

    # --------------------------------------------------------------------------------
    def UnDo(self, evt):
        """撤销修改"""

        self.nb.GetCurrentPage().Undo()

    # --------------------------------------------------------------------------------
    def ReDo(self, evt):
        """重做撤销的修改"""

        self.nb.GetCurrentPage().Redo()


# ================================================================================
class ProjectTree(wx.TreeCtrl):
    """
    继承wx.GenericDirCtrl，并扩展其功能
    """

    TYPE_DIR = 0
    TYPE_FILE = 1

    # --------------------------------------------------------------------------------
    def __init__(self, parent):
        """
        ProjectTree的构造函数
        """

        wx.TreeCtrl.__init__(self, parent, -1, style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS,)

        self.parent = parent

        self.projectPath = ""       # 工程路径

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        self.AssignImageList(imglist)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OpenFolder)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OpenFile)

    # --------------------------------------------------------------------------------
    def SetProjectPath(self, path):
        """设置工程路径"""

        self.projectPath = path

        self.RefreshTree()

    # --------------------------------------------------------------------------------
    def RefreshTree(self):
        """刷新工程树"""

        self.DeleteAllItems()

        if len(self.projectPath) > 0 and os.path.isdir(self.projectPath):
            self.rootItem = self.AddRoot(self.projectPath, 1)
            self.SetItemHasChildren(self.rootItem, True)
            self.SetItemData(self.rootItem, {"type": self.TYPE_DIR, "path": self.projectPath})

            self.Expand(self.rootItem)

    # --------------------------------------------------------------------------------
    def OpenFolder(self, evt):
        """显示目录下的文件和文件夹"""

        parent = evt.GetItem()
        self.DeleteChildren(parent)

        path = self.GetItemData(parent)["path"]
        dirs = []
        files = []
        for item in os.listdir(path):
            subpath = os.path.join(path, item)
            if os.path.isdir(subpath):
                dirs.append(item)
            else:
                files.append(item)

        for dir in dirs:
            item = self.AppendItem(parent, dir, 0)
            self.SetItemHasChildren(item, True)
            self.SetItemData(item, {"type": self.TYPE_DIR, "path": os.path.join(path, dir)})

        for file in files:
            item = self.AppendItem(parent, file, 1)
            self.SetItemData(item, {"type": self.TYPE_FILE, "path": os.path.join(path, file)})

    # --------------------------------------------------------------------------------
    def OpenFile(self, evt):
        """左键双击事件处理"""

        itemData = self.GetItemData(self.GetSelection())
        if itemData['type'] == 1 and itemData['path'].endswith('.py'):
            # 创建编辑页
            self.parent.OpenFile(itemData['path'])


# ================================================================================
class PythonSTC(stc.StyledTextCtrl):
    """从wxPython的Demo中摘出来的Python代码编辑控件"""

    fold_symbols = 2
    faces = {'times': 'Times New Roman',
             'mono': 'Courier New',
             'helv': 'Arial',
             'other': 'Comic Sans MS',
             'size': 12,
             'size2': 10,
             }

    def __init__(self, parent, ID, filePath,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

        self.parent = parent
        self.filepath = filePath
        self.LoadFile(filePath)

        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0,0)

        self.SetViewWhiteSpace(False)

        # self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        # self.SetEdgeColumn(78)

        # Setup a margin to hold fold markers
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY,     "white", "black")

        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")

        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)

        # 显示行号
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 40)

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % self.faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % self.faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % self.faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % self.faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        # Python styles
        # Default
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % self.faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % self.faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % self.faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % self.faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % self.faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % self.faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % self.faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % self.faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % self.faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % self.faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % self.faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % self.faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % self.faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % self.faces)

        self.SetCaretForeground("BLUE")


        # register some images for use in the AutoComplete box.
        # self.RegisterImage(1, images.Smiles.GetBitmap())
        self.RegisterImage(2, wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16,16)))
        self.RegisterImage(3, wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16,16)))

    def OnKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()

        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                                 'show some suff, maybe parameters..\n\n'
                                 'fubar(param1, param2)')
            # Code completion
            else:
                #lst = []
                #for x in range(50000):
                #    lst.append('%05d' % x)
                #st = " ".join(lst)
                #print(len(st))
                #self.AutoCompShow(0, st)

                kw = keyword.kwlist[:]
                kw.append("zzzzzz?2")
                kw.append("aaaaa?2")
                kw.append("__init__?3")
                kw.append("zzaaaaa?2")
                kw.append("zzbaaaa?2")
                kw.append("this_is_a_longer_value")
                #kw.append("this_is_a_much_much_much_much_much_much_much_longer_value")

                kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                # Images are specified with a appended "?type"
                for i in range(len(kw)):
                    if kw[i] in keyword.kwlist:
                        kw[i] = kw[i] + "?1"

                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()


    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            #pt = self.PointFromPosition(braceOpposite)
            #self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            #print(pt)
            #self.Refresh(False)


    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)


    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1



    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1

        return line

    def SaveFile(self):
        """保存文件"""

        super().SaveFile(self.filepath)


# ================================================================================
class MainApp(wx.App):
    """主应用程序"""

    # --------------------------------------------------------------------------------
    def __init__(self):
        """构造函数"""

        wx.App.__init__(self)

        self.frame = None

    # --------------------------------------------------------------------------------
    def OnInit(self):
        """
        主应用程序初始化回调函数
        :return: True
        """

        self.SetAppName(APP_TITLE)
        self.frame = MainFrame(None)
        self.frame.Show()

        return True


# --------------------------------------------------------------------------------
def main():
    """主函数"""

    app = MainApp()
    app.MainLoop()


# ================================================================================
if __name__ == "__main__":
    main()
