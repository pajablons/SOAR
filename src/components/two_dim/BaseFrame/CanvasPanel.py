import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt


class CanvasPanel(wx.Panel):
    def __init__(self, parent, uid):
        wx.Panel.__init__(self, parent, uid)

        self.bg = plt.imread(r'C:\Users\pajab\Documents\MSGIS\GEOG656\Panda3dFinal\assets\Textures\Earth_TEXTURE_CM.tga')

        self.figure, self.axes = plt.subplots()
        self.axes.imshow(self.bg, extent=[-180, 180, -90, 90])
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.canvas.draw()
        self.canvas.flush_events()
        self.Fit()

    def updateLocations(self, locales, stations, targets):
        self.axes.clear()
        self.axes.imshow(self.bg, extent=[-180, 180, -90, 90])
        locales.plot(ax=self.axes, color='yellow')
        if stations is not None:
            stations.plot(ax=self.axes, color='cyan')
        if targets is not None:
            targets.plot(ax=self.axes, color='red')

        self.canvas.draw()
