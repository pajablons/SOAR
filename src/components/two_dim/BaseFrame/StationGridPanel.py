from wx.grid import Grid
import wx


class StationGridPanel(wx.Panel):
    def __init__(self, parent, pid, type):
        super().__init__(parent, pid)
        self.data = {}

        self.grid = Grid(self, -1)
        self.makeGrid(self.grid)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(wx.StaticText(self, -1, type, style=wx.ALIGN_CENTER))
        self.sizer.Add(self.grid, 1, wx.GROW)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.sizer.Layout()

    def makeGrid(self, grid):
        grid.CreateGrid(0, 4)
        grid.SetColLabelValue(0, 'ID')
        grid.SetColLabelValue(1, 'Latitude')
        grid.SetColLabelValue(2, 'Longitude')
        grid.SetColLabelValue(3, 'Satellites Seen')

    def updateLocations(self, gdf):
        for index, row in gdf.iterrows():
            if index not in self.data.keys():
                self.addEntity(index)
            table_row = self.data[index]
            self.grid.SetCellValue(row=table_row, col=0, s=str(index))
            self.grid.SetCellValue(row=table_row, col=1, s='%.4f' % row['lat'])
            self.grid.SetCellValue(row=table_row, col=2, s='%.4f' % row['long'])
            if len(row['satellites']) > 0:
                self.grid.SetCellValue(row=table_row, col=3, s=str(row['satellites']))

    def addEntity(self, eid):
        if eid not in self.data.keys():
            self.data[eid] = len(self.data.keys())
            self.grid.AppendRows(1)
            self.grid.Layout()
            self.sizer.Layout()
            self.grid.AutoSize()
            return self.data[eid]
