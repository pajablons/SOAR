import wx


# wx wrapper panel for the panda display
class PandaPanel(wx.Panel):
    def __init__(self, parent, uid):
        wx.Panel.__init__(self, parent, uid)
        self.SetBackgroundColour('BLUE')
