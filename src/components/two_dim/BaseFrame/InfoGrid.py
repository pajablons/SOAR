from wx import Panel
import wx

from src.components.two_dim.BaseFrame.SatelliteGridPanel import SatelliteGridPanel
from src.components.two_dim.BaseFrame.StationGridPanel import StationGridPanel


class InfoGrid(Panel):
    def __init__(self, parent, pid):
        super().__init__(parent, pid)
        self.satPane = SatelliteGridPanel(self, -1)
        self.stationPane = StationGridPanel(self, -1, 'Stations')
        self.targetPane = StationGridPanel(self, -1, 'Targets')

        self.sizer = wx.GridSizer(3, 1, 15, 15)
        self.sizer.Add(self.satPane, 1, wx.EXPAND)
        self.sizer.Add(self.stationPane, 1, wx.EXPAND)
        self.sizer.Add(self.targetPane, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def updateLocations(self, sats, stations, targs):
        self.satPane.updateLocations(sats)
        self.stationPane.updateLocations(stations)
        self.targetPane.updateLocations(targs)