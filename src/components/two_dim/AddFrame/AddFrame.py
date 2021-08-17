import wx

from src.components.two_dim.AddFrame.MarkerInputPanel import MarkerInputPanel
from src.components.two_dim.AddFrame.SatelliteInputPanel import SatelliteInputPanel


class IllegalCoordinateException(Exception):
    pass


class AddFrame(wx.Frame):
    def __init__(self, parent, type):
        super().__init__(parent, wx.ID_ANY, title='Add Entity', size=(500, 300))

        self.type = type
        self.parentFrame = parent

        self.input_panel = SatelliteInputPanel(self) if type == 'SATELLITE' else MarkerInputPanel(self)
        self.errorText = wx.StaticText(self, -1, '', style=wx.ALIGN_CENTER, size=(100, 30))
        self.confirmButton = wx.Button(self, 103, label='Add')
        self.Bind(wx.EVT_BUTTON, self.button_clicked)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.input_panel, -1, wx.EXPAND)
        self.sizer.Add(self.errorText, -1, wx.FIXED_MINSIZE)
        self.sizer.Add(self.confirmButton, -1, wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)

        self.Show(True)

    def button_clicked(self, event):
        if event.GetId() == 103:
            try:
                latInput = float(self.input_panel.latInput.GetValue())
                longInput = float(self.input_panel.longInput.GetValue())
                if not (-90 <= latInput <= 90 and -180 <= longInput <= 180):
                    raise IllegalCoordinateException

                if self.type == 'BASESTATION':
                    self.parentFrame.soar.addBaseStation((
                        longInput,
                        latInput
                    ))
                elif self.type == 'TARGET':
                    self.parentFrame.soar.addTarget((
                        longInput,
                        latInput
                    ))
                elif self.type == 'SATELLITE':
                    latSpeedInput = float(self.input_panel.latSpeedInput.GetValue())
                    longSpeedInput = float(self.input_panel.longSpeedInput.GetValue())
                    self.parentFrame.soar.addSatellite(
                        (longInput, latInput),
                        (longSpeedInput, latSpeedInput)
                    )
                self.Close(True)
            except ValueError:
                self.errorText.SetLabelText('Lat/long must be of type Float')
            except IllegalCoordinateException:
                self.errorText.SetLabelText('Lat & Long must be in ranges [-90, 90] and [-180, 180]')
