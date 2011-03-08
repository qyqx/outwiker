# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Mar 23 21:59:58 2010

import os.path
import sys

import wx
import wx.aui

from core.tree import WikiDocument, RootWikiPage
from WikiTree import WikiTree
from gui.CurrentPagePanel import CurrentPagePanel
import core.commands
from core.recent import RecentWiki
import pages.search.searchpage
import core.system
from gui.preferences.PrefDialog import PrefDialog
from core.application import Application
from gui.trayicon import OutwikerTrayIcon
from gui.AttachPanel import AttachPanel
import core.config
import gui.pagedialog
from guiconfig import MainWindowConfig, TreeConfig, AttachConfig, GeneralGuiConfig

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade


class MainWindow(wx.Frame):
	def makeId (self):
		self.ID_NEW = wx.NewId()
		self.ID_OPEN = wx.NewId()
		self.ID_OPEN_READONLY = wx.NewId()
		self.ID_SAVE = wx.NewId()
		self.ID_SAVEAS = wx.NewId()
		self.ID_RELOAD = wx.NewId()
		self.ID_ADDPAGE = wx.NewId()
		self.ID_ADDCHILD = wx.NewId()
		self.ID_ATTACH = wx.NewId()
		self.ID_ABOUT = wx.NewId()
		self.ID_EXIT = wx.NewId()
		self.ID_COPYPATH = wx.NewId()
		self.ID_COPY_ATTACH_PATH = wx.NewId()
		self.ID_COPY_LINK = wx.NewId()
		self.ID_COPY_TITLE = wx.NewId()
		self.ID_BOOKMARKS = wx.NewId()
		self.ID_ADDBOOKMARK = wx.NewId()
		self.ID_EDIT = wx.NewId()
		self.ID_REMOVE_PAGE = wx.NewId()
		self.ID_GLOBAL_SEARCH = wx.NewId()
		self.ID_RENAME = wx.NewId()
		self.ID_HELP = wx.NewId()
		self.ID_PREFERENCES = wx.NewId()
		self.ID_VIEW_TREE = wx.NewId()
		self.ID_VIEW_ATTACHES = wx.NewId()
		self.ID_VIEW_FULLSCREEN = wx.NewId()
		self.ID_MOVE_PAGE_UP = wx.NewId()
		self.ID_MOVE_PAGE_DOWN = wx.NewId()
		self.ID_SORT_CHILDREN_ALPHABETICAL = wx.NewId()
		self.ID_SORT_SIBLINGS_ALPHABETICAL = wx.NewId()


	def __init__(self, *args, **kwds):
		self.makeId()

		self.disabledTools = [self.ID_SAVE, self.ID_SAVEAS, self.ID_RELOAD, 
				self.ID_ADDPAGE, self.ID_ADDCHILD, self.ID_ATTACH, 
				self.ID_COPYPATH, self.ID_COPY_ATTACH_PATH, self.ID_COPY_LINK,
				self.ID_COPY_TITLE, self.ID_BOOKMARKS, self.ID_ADDBOOKMARK,
				self.ID_EDIT, self.ID_REMOVE_PAGE, self.ID_GLOBAL_SEARCH,
				wx.ID_UNDO, wx.ID_REDO, wx.ID_CUT, wx.ID_COPY, wx.ID_PASTE,
				self.ID_SORT_SIBLINGS_ALPHABETICAL, self.ID_SORT_CHILDREN_ALPHABETICAL,
				self.ID_MOVE_PAGE_UP, self.ID_MOVE_PAGE_DOWN, self.ID_RENAME]


		self.mainWindowConfig = MainWindowConfig (Application.config)
		self.treeConfig = TreeConfig (Application.config)
		self.attachConfig = AttachConfig (Application.config)
		self.generalConfig = GeneralGuiConfig (Application.config)

		# Флаг, обозначающий, что в цикле обработки стандартных сообщений 
		# вроде копирования в буфер обмена сообщение вернулось обратно
		self.stdEventLoop = False

		# Идентификаторы для пунктов меню последних открытых вики
		# Ключ - id, значение - путь до вики
		self._recentId = {}

		# Идентификаторы для пунктов меню для открытия закладок
		# Ключ - id, значение - путь до страницы вики
		self._bookmarksId = {}

		Application.onTreeUpdate += self.onTreeUpdate
		Application.onPageSelect += self.onPageSelect
		Application.onBookmarksChanged += self.onBookmarksChanged
		Application.onMainWindowConfigChange += self.onMainWindowConfigChange
		
		# Путь к директории с программой/скриптом
		self.imagesDir = core.system.getImagesDir()

		# begin wxGlade: MainWindow.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		
		# Menu Bar
		self.mainMenu = wx.MenuBar()
		self.fileMenu = wx.Menu()
		self.fileMenu.Append(self.ID_NEW, _("&New\tCtrl+N"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN, _(u"&Open…\tCtrl+O"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN_READONLY, _(u"Open &Read-only…\tCtrl+Shift+O"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_SAVE, _("&Save\tCtrl+S"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_EXIT, _(u"&Exit…\tAlt+F4"), "", wx.ITEM_NORMAL)
		self.fileMenu.AppendSeparator()
		self.mainMenu.Append(self.fileMenu, _("&File"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_UNDO, _("&Undo\tCtrl+Z"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_REDO, _("&Redo\tCtrl+Y"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(wx.ID_CUT, _("Cu&t\tCtrl+X"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_COPY, _("&Copy\tCtrl+C"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_PASTE, _("&Paste\tCtrl+V"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_PREFERENCES, _(u"Pr&eferences…\tCtrl+F8"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, _("&Edit"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_ADDPAGE, _(u"Add &Sibling Page…\tCtrl+T"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ADDCHILD, _(u"Add &Child Page…\tCtrl+Shift+T"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_MOVE_PAGE_UP, _("Move Page Up\tCtrl+Shift+Up"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_MOVE_PAGE_DOWN, _("Move Page Down\tCtrl+Shift+Down"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_SORT_CHILDREN_ALPHABETICAL, _("Sort Children Pages Alphabetical"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_SORT_SIBLINGS_ALPHABETICAL, _("Sort Siblings Pages Alphabetical"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_RENAME, _("Re&name Page\tF2"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_REMOVE_PAGE, _(u"Rem&ove Page…\tCtrl+Shift+Del"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_EDIT, _(u"&Edit Page Properties…\tCtrl+E"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, _("&Tree"))
		self.toolsMenu = wx.Menu()
		self.toolsMenu.Append(self.ID_GLOBAL_SEARCH, _(u"&Global Search…\tCtrl+Shift+F"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_ATTACH, _(u"&Attach Files…\tCtrl+Alt+A"), "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_COPY_TITLE, _("Copy Page &Title\tCtrl+Shift+D"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPYPATH, _("Copy &Page Path\tCtrl+Shift+P"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_ATTACH_PATH, _("Copy Atta&ches Path\tCtrl+Shift+A"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_LINK, _("Copy Page &Link\tCtrl+Shift+L"), "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_RELOAD, _(u"&Reload Wiki…\tCtrl+R"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(self.toolsMenu, _("T&ools"))
		self.bookmarksMenu = wx.Menu()
		self.bookmarksMenu.Append(self.ID_ADDBOOKMARK, _("&Add/Remove Bookmark\tCtrl+D"), "", wx.ITEM_NORMAL)
		self.bookmarksMenu.AppendSeparator()
		self.mainMenu.Append(self.bookmarksMenu, _("&Bookmarks"))
		wxglade_tmp_menu = wx.Menu()
		self.viewNotes = wx.MenuItem(wxglade_tmp_menu, self.ID_VIEW_TREE, _("Notes &Tree"), "", wx.ITEM_CHECK)
		wxglade_tmp_menu.AppendItem(self.viewNotes)
		self.viewAttaches = wx.MenuItem(wxglade_tmp_menu, self.ID_VIEW_ATTACHES, _("Attaches"), "", wx.ITEM_CHECK)
		wxglade_tmp_menu.AppendItem(self.viewAttaches)
		wxglade_tmp_menu.AppendSeparator()
		self.viewFullscreen = wx.MenuItem(wxglade_tmp_menu, self.ID_VIEW_FULLSCREEN, _("Fullscreen\tF11"), "", wx.ITEM_CHECK)
		wxglade_tmp_menu.AppendItem(self.viewFullscreen)
		self.mainMenu.Append(wxglade_tmp_menu, _("&View"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_HELP, _("&Help\tF1"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ABOUT, _(u"&About…\tCtrl+F1"), "", wx.ITEM_NORMAL)
		self.mainMenu.Append(wxglade_tmp_menu, _("&Help"))
		self.SetMenuBar(self.mainMenu)
		# Menu Bar end
		
		# Tool Bar
		self.mainToolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE)
		self.SetToolBar(self.mainToolbar)
		self.mainToolbar.AddLabelTool(self.ID_NEW, _(u"New…"), wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Create new wiki…"), "")
		self.mainToolbar.AddLabelTool(self.ID_OPEN, _(u"Open…"), wx.Bitmap(os.path.join (self.imagesDir, "open.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Open wiki…"), "")
		self.mainToolbar.AddLabelTool(self.ID_SAVE, _("Save"), wx.Bitmap(os.path.join (self.imagesDir, "save.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Save wiki"), "")
		self.mainToolbar.AddLabelTool(self.ID_RELOAD, _("Reload"), wx.Bitmap(os.path.join (self.imagesDir, "reload.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Reload wiki"), "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(self.ID_ATTACH, _(u"Attach files…"), wx.Bitmap(os.path.join (self.imagesDir, "attach.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Attach files…"), "")
		self.mainToolbar.AddLabelTool(self.ID_EDIT, _("Edit page"), wx.Bitmap(os.path.join (self.imagesDir, "edit.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Edit page's properties"), "")
		self.mainToolbar.AddLabelTool(self.ID_GLOBAL_SEARCH, _(u"Global search…"), wx.Bitmap(os.path.join (self.imagesDir, "global_search.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Global search…"), "")
		self.mainToolbar.AddSeparator()
		# Tool Bar end
		self.mainPanel = wx.Panel(self, -1)
		self.statusbar = wx.StatusBar(self, -1)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_MENU, self.onNew, id=self.ID_NEW)
		self.Bind(wx.EVT_MENU, self.onOpen, id=self.ID_OPEN)
		self.Bind(wx.EVT_MENU, self.onOpenReadOnly, id=self.ID_OPEN_READONLY)
		self.Bind(wx.EVT_MENU, self.onSave, id=self.ID_SAVE)
		self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_UNDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_REDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_CUT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_COPY)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_PASTE)
		self.Bind(wx.EVT_MENU, self.onPreferences, id=self.ID_PREFERENCES)
		self.Bind(wx.EVT_MENU, self.onAddSiblingPage, id=self.ID_ADDPAGE)
		self.Bind(wx.EVT_MENU, self.onAddChildPage, id=self.ID_ADDCHILD)
		self.Bind(wx.EVT_MENU, self.onMovePageUp, id=self.ID_MOVE_PAGE_UP)
		self.Bind(wx.EVT_MENU, self.onMovePageDown, id=self.ID_MOVE_PAGE_DOWN)
		self.Bind(wx.EVT_MENU, self.onSortChildrenAlphabetical, id=self.ID_SORT_CHILDREN_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.onSortSiblingAlphabetical, id=self.ID_SORT_SIBLINGS_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.onRename, id=self.ID_RENAME)
		self.Bind(wx.EVT_MENU, self.onRemovePage, id=self.ID_REMOVE_PAGE)
		self.Bind(wx.EVT_MENU, self.onEditPage, id=self.ID_EDIT)
		self.Bind(wx.EVT_MENU, self.onGlobalSearch, id=self.ID_GLOBAL_SEARCH)
		self.Bind(wx.EVT_MENU, self.onAttach, id=self.ID_ATTACH)
		self.Bind(wx.EVT_MENU, self.onCopyTitle, id=self.ID_COPY_TITLE)
		self.Bind(wx.EVT_MENU, self.onCopyPath, id=self.ID_COPYPATH)
		self.Bind(wx.EVT_MENU, self.onCopyAttaches, id=self.ID_COPY_ATTACH_PATH)
		self.Bind(wx.EVT_MENU, self.onCopyLink, id=self.ID_COPY_LINK)
		self.Bind(wx.EVT_MENU, self.onReload, id=self.ID_RELOAD)
		self.Bind(wx.EVT_MENU, self.onBookmark, id=self.ID_ADDBOOKMARK)
		self.Bind(wx.EVT_MENU, self.onViewTree, self.viewNotes)
		self.Bind(wx.EVT_MENU, self.onViewAttaches, self.viewAttaches)
		self.Bind(wx.EVT_MENU, self.onFullscreen, self.viewFullscreen)
		self.Bind(wx.EVT_MENU, self.onHelp, id=self.ID_HELP)
		self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)
		self.Bind(wx.EVT_TOOL, self.onNew, id=self.ID_NEW)
		self.Bind(wx.EVT_TOOL, self.onOpen, id=self.ID_OPEN)
		self.Bind(wx.EVT_TOOL, self.onReload, id=self.ID_RELOAD)
		self.Bind(wx.EVT_TOOL, self.onAttach, id=self.ID_ATTACH)
		self.Bind(wx.EVT_TOOL, self.onEditPage, id=self.ID_EDIT)
		self.Bind(wx.EVT_TOOL, self.onGlobalSearch, id=self.ID_GLOBAL_SEARCH)
		# end wxGlade

		Application.onWikiOpen += self.onWikiOpen

		self.auiManager = wx.aui.AuiManager(self.mainPanel)

		self.tree = WikiTree(self.mainPanel, -1)
		self.pagePanel = CurrentPagePanel(self.mainPanel, -1)
		self.attachPanel = AttachPanel (self.mainPanel, -1)

		self.__loadMainWindowParams()
		self.__initAuiManager ()
		self.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.onPaneClose)

		self.__setMenuBitmaps()
		
		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.mainPanel.Bind (wx.EVT_CLOSE, self.onMainPanelClose)

		self._dropTarget = DropFilesTarget (self)

		self.__enableGui()

		self.statusbar.SetFieldsCount(1)

		aTable = wx.AcceleratorTable([
			(wx.ACCEL_CTRL,  wx.WXK_INSERT, wx.ID_COPY),
			(wx.ACCEL_SHIFT,  wx.WXK_INSERT, wx.ID_PASTE),
			(wx.ACCEL_SHIFT,  wx.WXK_DELETE, wx.ID_CUT)])
		self.SetAcceleratorTable(aTable)

		self._updateRecentMenu()
		self.setFullscreen(self.mainWindowConfig.FullscreenOption.value)

		if len (sys.argv) > 1:
			self._openFromCommandLine()
		else:
			# Открыть последний открытый файл (если установлена соответствующая опция)
			self.__openRecentWiki ()

		self.taskBarIcon = OutwikerTrayIcon(self)
		self.__updateTitle()

	
	def onWikiOpen (self, wikiroot):
		"""
		Обновить окно после того как загрузили вики
		"""
		if wikiroot != None and not wikiroot.readonly:
			self.recentWiki.add (wikiroot.path)
			self._updateRecentMenu()

		self.__enableGui()
		self._loadBookmarks()
		self.__updateTitle()


	def onMainPanelClose (self, event):
		self.tree.Close()
		self.tree = None

		self.pagePanel.Close()
		self.pagePanel = None

		self.attachPanel.Close()
		self.attachPanel = None
		
		self.mainPanel.Destroy()


	def __initAuiManager(self):
		self.__initPagePane (self.auiManager)
		self.__initAttachesPane (self.auiManager)
		self.__initTreePane (self.auiManager)

		self.auiManager.SetDockSizeConstraint (0.8, 0.8)
		self.auiManager.Update()

	
	def onPaneClose (self, event):
		if event.GetPane().name == self.auiManager.GetPane (self.tree).name:
			self.viewNotes.Check (False)
		elif event.GetPane().name == self.auiManager.GetPane (self.attachPanel).name:
			self.viewAttaches.Check (False)


	def __initTreePane (self, auiManager):
		"""
		Загрузить настройки окошка с деревом
		"""
		pane = self.__loadPaneInfo (self.treeConfig.treePaneOption)

		if pane == None:
			pane = wx.aui.AuiPaneInfo().Name(("treePane")).Caption(_("Notes")).Gripper(False).CaptionVisible(True).Layer(2).Position(0).CloseButton(True).MaximizeButton(False).Left().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		pane.CloseButton()

		pane.BestSize ((self.treeConfig.treeWidthOption.value, 
			self.treeConfig.treeHeightOption.value))
		
		auiManager.AddPane(self.tree, pane)
	

	def __initAttachesPane (self, auiManager):
		"""
		Загрузить настройки окошка с прикрепленными файлами
		"""
		pane = self.__loadPaneInfo (self.attachConfig.attachesPaneOption)

		if pane == None:
			pane = wx.aui.AuiPaneInfo().Name("attachesPane").Caption(_("Attaches")).Gripper(False).CaptionVisible(True).Layer(1).Position(0).CloseButton(True).MaximizeButton(False).Bottom().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		pane.CloseButton()

		auiManager.AddPane(self.attachPanel, pane, _('Attaches') )
	

	def __initPagePane (self, auiManager):
		"""
		Загрузить настройки окошка с видом текущей страницы
		"""
		pane = wx.aui.AuiPaneInfo().Name("pagePane").Gripper(False).CaptionVisible(False).Layer(0).Position(0).CloseButton(False).MaximizeButton(False).Center().Dock()

		auiManager.AddPane(self.pagePanel, pane)
	

	def __loadPaneInfo (self, param):
		"""
		Загрузить из конфига и вернуть информацию о dockable-панели (AuiPaneInfo)
		"""
		string_info = param.value

		if len (string_info) == 0:
			return

		pane = wx.aui.AuiPaneInfo()
		try:
			self.auiManager.LoadPaneInfo (string_info, pane)
		except Exception, e:
			return

		return pane


	def __savePaneInfo (self, param, paneInfo):
		"""
		Сохранить в конфиг информацию о dockable-панели (AuiPaneInfo)
		"""
		string_info = self.auiManager.SavePaneInfo (paneInfo)
		param.value = string_info


	def __savePanesParams (self):
		"""
		Сохранить параметры панелей
		"""
		self.__savePaneInfo (self.treeConfig.treePaneOption, self.auiManager.GetPane (self.tree))
		self.__savePaneInfo (self.attachConfig.attachesPaneOption, self.auiManager.GetPane (self.attachPanel))
		self.__savePanesSize()
	

	def __savePanesSize (self):
		"""
		Сохранить размеры панелей
		"""
		self.treeConfig.treeWidthOption.value = self.tree.GetSizeTuple()[0]
		self.treeConfig.treeHeightOption.value = self.tree.GetSizeTuple()[1]
			
		self.attachConfig.attachesWidthOption.value = self.attachPanel.GetSizeTuple()[0]
		self.attachConfig.attachesHeightOption.value = self.attachPanel.GetSizeTuple()[1]


	def onPageSelect (self, newpage):
		self.__updateTitle()
	

	def __updateTitle (self):
		template = self.mainWindowConfig.titleFormatOption.value

		if Application.wikiroot == None:
			self.SetTitle (u"OutWiker")
			return

		pageTitle = u"" if Application.wikiroot.selectedPage == None else Application.wikiroot.selectedPage.title
		filename = os.path.basename (Application.wikiroot.path)

		result = template.replace ("{file}", filename).replace ("{page}", pageTitle)
		self.SetTitle (result)
	

	def __enableGui (self):
		"""
		Проверить открыта ли вики и включить или выключить кнопки на панели
		"""
		enabled = Application.wikiroot != None
		self.__enableTools (enabled)
		self.__enableMenu (enabled)
		self.pagePanel.Enable(enabled)
		self.tree.Enable(enabled)
		self.attachPanel.Enable(enabled)


	
	def __enableTools (self, enabled):
		for toolId in self.disabledTools:
			if self.mainToolbar.FindById (toolId) != None:
				self.mainToolbar.EnableTool (toolId, enabled)

	
	def __enableMenu (self, enabled):
		for toolId in self.disabledTools:
			if self.mainMenu.FindItemById (toolId) != None:
				self.mainMenu.Enable (toolId, enabled)


	def __setMenuBitmaps (self):
		newItem = self.fileMenu.FindItemById (self.ID_NEW)
		newBitmap = wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY)
		newItem.SetBitmap (newBitmap)


	def __openRecentWiki (self):
		"""
		Открыть последнюю вики, если установлена соответствующая опция
		"""
		openRecent = self.generalConfig.autoopenOption.value

		if openRecent and len (self.recentWiki) > 0:
			core.commands.openWiki (self.recentWiki[0])


	def _openFromCommandLine (self):
		"""
		Открыть вики, путь до которой передан в командной строке
		"""
		fname = unicode (sys.argv[1], core.system.getOS().filesEncoding)
		if not os.path.isdir (fname):
			fname = os.path.split (fname)[0]

		core.commands.openWiki (fname)

	
	def _updateRecentMenu (self):
		"""
		Обновление меню со списком последних открытых вики
		"""
		self._removeMenuItemsById (self.fileMenu, self._recentId.keys())
		self._recentId = {}

		# TODO: Рефакторинг
		# Сделать класс RecentWiki изменяемым
		self.recentWiki = RecentWiki (Application.config)

		self._recentId = {}

		for n in range (len (self.recentWiki)):
			id = wx.NewId()
			path = self.recentWiki[n]
			self._recentId[id] = path

			title = path if n + 1 > 9 else u"&{n}. {path}".format (n=n + 1, path=path)

			self.fileMenu.Append (id, title, "", wx.ITEM_NORMAL)
			
			self.Bind(wx.EVT_MENU, self.onRecent, id=id)
	

	def _loadBookmarks (self):
		self._removeMenuItemsById (self.bookmarksMenu, self._bookmarksId.keys())
		self._bookmarksId = {}

		if Application.wikiroot != None:
			for n in range (len (Application.wikiroot.bookmarks)):
				id = wx.NewId()
				page = Application.wikiroot.bookmarks[n]
				if page == None:
					continue

				subpath = page.subpath
				self._bookmarksId[id] = subpath

				# Найдем родителя
				parent = page.parent

				if parent.parent != None:
					label = "%s [%s]" % (page.title, parent.subpath)
				else:
					label = page.title

				self.bookmarksMenu.Append (id, label, "", wx.ITEM_NORMAL)
				self.Bind(wx.EVT_MENU, self.onSelectBookmark, id=id)


	def _removeMenuItemsById (self, menu, keys):
		"""
		Удалить все элементы меню по идентификаторам
		"""
		for key in keys:
			menu.Delete (key)
			self.Unbind (wx.EVT_MENU, id = key)


	def onRecent (self, event):
		"""
		Выбор пункта меню с недавно открытыми файлами
		"""
		core.commands.openWiki (self._recentId[event.Id])


	def onSelectBookmark (self, event):
		subpath = self._bookmarksId[event.Id]
		page = Application.wikiroot[subpath]

		if page != None:
			Application.wikiroot.selectedPage = Application.wikiroot[subpath]
	

	def __loadMainWindowParams(self):
		"""
		Загрузить параметры из конфига
		"""
		#config = Application.config
		self.Freeze()

		width = self.mainWindowConfig.WidthOption.value
		height = self.mainWindowConfig.HeightOption.value

		xpos = self.mainWindowConfig.XPosOption.value
		ypos = self.mainWindowConfig.YPosOption.value
		
		self.SetDimensions (xpos, ypos, width, height, sizeFlags=wx.SIZE_FORCE)

		self.Layout()
		self.Thaw()
	

	def __saveParams (self):
		"""
		Сохранить параметры в конфиг
		"""
		#config = Application.config

		try:
			if not self.IsIconized():
				if not self.IsFullScreen():
					(width, height) = self.GetSizeTuple()
					self.mainWindowConfig.WidthOption.value = width
					self.mainWindowConfig.HeightOption.value = height

					(xpos, ypos) = self.GetPositionTuple()
					self.mainWindowConfig.XPosOption.value = xpos
					self.mainWindowConfig.YPosOption.value = ypos

				self.mainWindowConfig.FullscreenOption.value = self.IsFullScreen()

				self.__savePanesParams()
		except Exception, e:
			core.commands.MessageBox (_(u"Can't save config\n%s") % (unicode (e)), 
					_(u"Error"), wx.ICON_ERROR | wx.OK)
	

	def __set_properties(self):
		# begin wxGlade: MainWindow.__set_properties
		self.SetTitle(_("OutWiker"))
		_icon = wx.EmptyIcon()
		_icon.CopyFromBitmap(wx.Bitmap(os.path.join (self.imagesDir, "icon.ico"), wx.BITMAP_TYPE_ANY))
		self.SetIcon(_icon)
		self.mainToolbar.Realize()
		# end wxGlade


	def __do_layout(self):
		# begin wxGlade: MainWindow.__do_layout
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		mainSizer.Add(self.mainPanel, 1, wx.EXPAND, 0)
		mainSizer.Add(self.statusbar, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)
		self.Layout()
		# end wxGlade


	def onClose (self, event):
		askBeforeExit = self.generalConfig.askBeforeExitOption.value

		if (not askBeforeExit or 
				core.commands.MessageBox (_(u"Really exit?"), _(u"Exit"), wx.YES_NO  | wx.ICON_QUESTION ) == wx.YES):
			self.__saveParams()

			self.auiManager.UnInit()
			self.mainPanel.Close()

			self.taskBarIcon.Destroy()
			self.Destroy()
		else:
			event.Veto()
	

	def onMainWindowConfigChange (self):
		self.__updateTitle()


	def onTreeUpdate (self, sender):
		"""
		Событие при обновлении дерева
		"""
		self._loadBookmarks()


	def onNew(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.createNewWiki(self)


	def onOpen(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.openWikiWithDialog (self)
	

	def onSave(self, event): # wxGlade: MainWindow.<event_handler>
		Application.onForceSave()


	def onReload(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.reloadWiki (self)
	

	def destroyPagePanel (self, save):
		"""
		Уничтожить панель с текущей страницей.
		save - надо ли предварительно сохранить страницу?
		"""
		if save:
			self.pagePanel.destroyPageView()
		else:
			self.pagePanel.destroyWithoutSave()


	def onAddSiblingPage(self, event): # wxGlade: MainWindow.<event_handler>
		"""
		Создание страницы на уровне текущей страницы
		"""
		gui.pagedialog.createSiblingPage (self)

	
	def onAddChildPage(self, event): # wxGlade: MainWindow.<event_handler>
		"""
		Создание дочерней страницы
		"""
		gui.pagedialog.createChildPage (self)


	def onAttach(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			core.commands.attachFilesWithDialog (self, Application.wikiroot.selectedPage)

	def onAbout(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.showAboutDialog (self)


	def onExit(self, event): # wxGlade: MainWindow.<event_handler>
		self.Close()


	def onCopyPath(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			core.commands.copyPathToClipboard (Application.wikiroot.selectedPage)


	def onCopyAttaches(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			core.commands.copyAttachPathToClipboard (Application.wikiroot.selectedPage)

	
	def onCopyLink(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			core.commands.copyLinkToClipboard (Application.wikiroot.selectedPage)

	
	def onCopyTitle(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			core.commands.copyTitleToClipboard (Application.wikiroot.selectedPage)
	

	def onBookmarksChanged (self, event):
		self._loadBookmarks()


	def onBookmark(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			selectedPage = Application.wikiroot.selectedPage

			if not Application.wikiroot.bookmarks.pageMarked (selectedPage):
				Application.wikiroot.bookmarks.add (Application.wikiroot.selectedPage)
			else:
				Application.wikiroot.bookmarks.remove (Application.wikiroot.selectedPage)


	def onEditPage(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			core.commands.editPage (self, Application.wikiroot.selectedPage)


	def onRemovePage(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.selectedPage != None:
			core.commands.removePage (Application.wikiroot.selectedPage)


	@core.commands.testreadonly
	def onGlobalSearch(self, event): # wxGlade: MainWindow.<event_handler>
		if Application.wikiroot != None:
			try:
				pages.search.searchpage.GlobalSearch.create (Application.wikiroot)
			except IOError:
				core.commands.MessageBox (_(u"Can't create page"), _(u"Error"), wx.ICON_ERROR | wx.OK)


	def onStdEvent(self, event): # wxGlade: MainWindow.<event_handler>
		if not self.stdEventLoop:
			self.stdEventLoop = True
			target = wx.Window.FindFocus()
			target.ProcessEvent (event)
		self.stdEventLoop = False


	def onRename(self, event): # wxGlade: MainWindow.<event_handler>
		self.tree.beginRename()


	def onHelp(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.openHelp()


	def onOpenReadOnly(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.openWikiWithDialog (self, readonly=True)


	def onPreferences(self, event): # wxGlade: MainWindow.<event_handler>
		dlg = PrefDialog (self)
		dlg.ShowModal()
		dlg.Destroy()
	

	def onViewTree(self, event): # wxGlade: MainWindow.<event_handler>
		self.showHideTree()
	

	def __showHidePane (self, control):
		"""
		Показать / скрыть pane с некоторым контролом
		"""
		pane = self.auiManager.GetPane (control)

		self.__savePanesSize()

		if pane.IsShown():
			pane.Hide()
		else:
			pane.Show()

		self.__loadPanesSize ()
		self.__updateViewMenu()
	

	def showHideTree (self):
		"""
		Показать/спарятать дерево с заметками
		"""
		self.__showHidePane (self.tree)

	
	def showHideAttaches (self):
		"""
		Показать/спарятать дерево с заметками
		"""
		self.__showHidePane (self.attachPanel)


	def onViewAttaches(self, event): # wxGlade: MainWindow.<event_handler>
		self.showHideAttaches()


	def onFullscreen(self, event): # wxGlade: MainWindow.<event_handler>
		self.setFullscreen(not self.IsFullScreen())


	def setFullscreen (self, fullscreen):
		"""
		Установить параметры в зависимости от режима fullscreen
		"""
		if fullscreen:
			self.__toFullscreen()
		else:
			self.__fromFullscreen()


	def __toFullscreen(self):
		self.__savePanesSize()
		self.ShowFullScreen(True, wx.FULLSCREEN_NOTOOLBAR | wx.FULLSCREEN_NOBORDER | wx.FULLSCREEN_NOCAPTION)
		self.auiManager.GetPane (self.attachPanel).Hide()
		self.auiManager.GetPane (self.tree).Hide()
		self.auiManager.Update()
		self.__updateViewMenu()


	def __fromFullscreen (self):
		self.__loadMainWindowParams()
		self.ShowFullScreen(False)
		self.auiManager.GetPane (self.attachPanel).Show()
		self.auiManager.GetPane (self.tree).Show()
		self.__loadPanesSize ()
		self.__updateViewMenu()

	
	def __loadPanesSize (self):
		self.auiManager.GetPane (self.attachPanel).BestSize ((self.attachConfig.attachesWidthOption.value, 
			self.attachConfig.attachesHeightOption.value))

		self.auiManager.GetPane (self.tree).BestSize ((self.treeConfig.treeWidthOption.value, 
			self.treeConfig.treeHeightOption.value))

		self.auiManager.Update()
	

	def __updateViewMenu (self):
		self.viewNotes.Check (self.auiManager.GetPane (self.tree).IsShown())
		self.viewAttaches.Check (self.auiManager.GetPane (self.attachPanel).IsShown())
		self.viewFullscreen.Check (self.IsFullScreen())


	def onMovePageUp(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.moveCurrentPageUp()


	def onMovePageDown(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.moveCurrentPageDown()
		

	def onSortChildrenAlphabetical(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.sortChildrenAlphabeticalGUI()


	def onSortSiblingAlphabetical(self, event): # wxGlade: MainWindow.<event_handler>
		core.commands.sortSiblingsAlphabeticalGUI()

# end of class MainWindow


class DropFilesTarget (wx.FileDropTarget):
	def __init__ (self, mainWindow):
		wx.FileDropTarget.__init__ (self)
		self._mainWindow = mainWindow
		self._mainWindow.SetDropTarget (self)
	
	
	def OnDropFiles (self, x, y, files):
		if (Application.wikiroot != None and
				Application.wikiroot.selectedPage != None):
			core.commands.attachFiles (self._mainWindow, 
						Application.wikiroot.selectedPage, 
						files)
			return True
