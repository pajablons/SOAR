import wx


class SatelliteInputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        self.sizer = wx.GridSizer(4, 2, 15, 15)

        self.latText = wx.StaticText(self, label='Latitude:')
        self.latInput = wx.TextCtrl(self, value='', size=(100, 40))
        self.longText = wx.StaticText(self, label='Longitude:')
        self.longInput = wx.TextCtrl(self, value='', size=(100, 40))
        self.latSpeedText = wx.StaticText(self, label='Lat Speed:')
        self.latSpeedInput = wx.TextCtrl(self, value='', size=(100, 40))
        self.longSpeedText = wx.StaticText(self, label='Long Speed:')
        self.longSpeedInput = wx.TextCtrl(self, value='', size=(100, 40))
        self.sizer.Add(self.latText, 1, wx.ALL)
        self.sizer.Add(self.latInput, 1, wx.ALL)
        self.sizer.Add(self.longText, 1, wx.ALL)
        self.sizer.Add(self.longInput, 1, wx.ALL)
        self.sizer.Add(self.latSpeedText, 1, wx.ALL)
        self.sizer.Add(self.latSpeedInput, 1, wx.ALL)
        self.sizer.Add(self.longSpeedText, 1, wx.ALL)
        self.sizer.Add(self.longSpeedInput, 1, wx.ALL)
        self.SetSizer(self.sizer)

