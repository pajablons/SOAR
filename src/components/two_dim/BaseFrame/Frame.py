import wx

from src.components.two_dim.AddFrame.AddFrame import AddFrame
from src.components.two_dim.BaseFrame.CanvasPanel import CanvasPanel
from src.components.two_dim.BaseFrame.InfoGrid import InfoGrid
from src.components.two_dim.BaseFrame.PandaPanel import PandaPanel


class Frame(wx.Frame):
    def __init__(self, soar_app):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Satellite Orbit AnalyzeR', size=(1920, 1080))

        self.soar = soar_app

        self.build_elements()
        self.init_layout()

        self.addFrame = None

        self.Fit()
        self.Layout()
        self.Show(True)

    def build_elements(self):
        menubar = wx.MenuBar()
        add_menu = wx.Menu()
        add_menu.Append(wx.MenuItem(add_menu, 100, text='Add Target', kind=wx.ITEM_DROPDOWN))
        add_menu.Append(wx.MenuItem(add_menu, 101, text='Add Station', kind=wx.ITEM_DROPDOWN))
        add_menu.Append(wx.MenuItem(add_menu, 102, text='Add Satellite', kind=wx.ITEM_DROPDOWN))
        menubar.Append(add_menu, '&Add Entities')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.menuhandler)

        self.panda_panel = PandaPanel(self, -1)
        self.right_panel = wx.Panel(self, -1)
        self.map_panel = CanvasPanel(self.right_panel, -1)
        self.info_grid = InfoGrid(self.right_panel, -1)

    def menuhandler(self, event):
        if self.addFrame is None and event.GetId() in [100, 101, 102]:
            if event.GetId() == 101:
                self.addFrame = AddFrame(self, 'BASESTATION')
            elif event.GetId() == 100:
                self.addFrame = AddFrame(self, 'TARGET')
            elif event.GetId() == 102:
                self.addFrame = AddFrame(self, 'SATELLITE')
            self.addFrame.Bind(wx.EVT_CLOSE, self.closeAddFrame)
        event.Skip()

    def closeAddFrame(self, event):
        self.addFrame = None
        event.Skip()

    def init_layout(self):
        horizontal_split = wx.GridSizer(1, 2, 15, 15)
        horizontal_split.Add(self.panda_panel, 1, wx.EXPAND)

        right_split = wx.GridSizer(2, 1, 15, 15)
        right_split.Add(self.map_panel, 1, wx.EXPAND)
        right_split.Add(self.info_grid, 1, wx.EXPAND)
        self.right_panel.SetSizer(right_split)
        horizontal_split.Add(self.right_panel, 1, wx.EXPAND)
        self.SetSizer(horizontal_split)

    def getPandaPanel(self):
        return self.panda_panel
