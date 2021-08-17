import wx


# Input panel for accepting data re: new markers (ie: basestations)
class MarkerInputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        # Basic layout: label column | input control
        # One row per input
        self.sizer = wx.GridSizer(2, 2, 15, 15)

        # We accept lat and long inputs
        self.latText = wx.StaticText(self, label='Latitude:')
        self.latInput = wx.TextCtrl(self, value='', size=(100, 30))
        self.longText = wx.StaticText(self, label='Longitude:')
        self.longInput = wx.TextCtrl(self, value='', size=(100, 30))
        self.sizer.Add(self.latText, 1, wx.ALL)
        self.sizer.Add(self.latInput, 1, wx.ALL)
        self.sizer.Add(self.longText, 1, wx.ALL)
        self.sizer.Add(self.longInput, 1, wx.ALL)
        self.SetSizer(self.sizer)

