from wx import Panel
import wx

from src.components.two_dim.BaseFrame.SatelliteGridPanel import SatelliteGridPanel
from src.components.two_dim.BaseFrame.StationGridPanel import StationGridPanel


# Info panel showing all the tracker info
class InfoGrid(Panel):
    def __init__(self, parent, pid):
        super().__init__(parent, pid)
        # Satellites have a litle more data so they have a separate panel type
        self.satPane = SatelliteGridPanel(self, -1)
        # Each marker type gets a display pane
        self.stationPane = StationGridPanel(self, -1, 'Stations')
        self.targetPane = StationGridPanel(self, -1, 'Targets')

        # Layout: Stacked vertically, 1 display grid per row
        self.sizer = wx.GridSizer(3, 1, 15, 15)
        self.sizer.Add(self.satPane, 1, wx.EXPAND)
        self.sizer.Add(self.stationPane, 1, wx.EXPAND)
        self.sizer.Add(self.targetPane, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    # Easy updater from the tracking manager
    # Pass the gdfs to each relevant subpane
    def updateLocations(self, sats, stations, targs):
        self.satPane.updateLocations(sats)
        self.stationPane.updateLocations(stations)
        self.targetPane.updateLocations(targs)
