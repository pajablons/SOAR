import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt


# Panel for displaying the 2d map representation
class CanvasPanel(wx.Panel):
    def __init__(self, parent, uid):
        wx.Panel.__init__(self, parent, uid)

        # The background of the map is a simple image of the earth
        self.bg = plt.imread(r'C:\Users\pajab\Documents\MSGIS\GEOG656\Panda3dFinal\assets\Textures\Earth_TEXTURE_CM.tga')

        # Build the empty figure
        self.figure, self.axes = plt.subplots()
        self.axes.imshow(self.bg, extent=[-180, 180, -90, 90])
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.canvas.draw()
        self.canvas.flush_events()
        self.Fit()

    # Update the locations of all entities on the map
    # Importantly, this is the biggest slowdown in the entire system.
    # Matplotlib is VERY slow about rendering geometries.  Agonizingly so.
    # A next step would be to throw out the matplotlib rendering and simply do our own
    # graphical updating, presumably through Pillow or something.  #TODO
    def updateLocations(self, locales, stations, targets):
        # Clear the previous rendering.  If we don't, we just accumulate a gazillion points.
        self.axes.clear()
        # Re-show the background image
        self.axes.imshow(self.bg, extent=[-180, 180, -90, 90])
        # Plot each set of geometries
        if not locales.empty:
            locales.plot(ax=self.axes, color='yellow')
        if stations is not None:
            stations.plot(ax=self.axes, color='cyan')
        if targets is not None:
            targets.plot(ax=self.axes, color='red')
