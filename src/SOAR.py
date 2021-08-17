import os

import wx
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
import panda3d.core as core

from src.TrackingManager import TrackingManager
from src.Util.AssetFactory import AssetFactory
from src.Util.Config import Config
from src.Util.TaskManager import TaskManager
from src.components.three_dim.BaseStation import BaseStation
from src.components.three_dim.EarthBase import EarthBase
from src.components.three_dim.Satellite import SatelliteEntity
from src.components.three_dim.TargetPoint import TargetPoint
from src.components.two_dim.BaseFrame.Frame import Frame


class SOAR(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.startWx()

        self.frame = Frame(self)
        self.pandaPanel = self.frame.getPandaPanel()

        wp = self.create_wp()
        self.openDefaultWindow(props=wp, gsg=None)
        self.frame.Show()

        self.pandaPanel.Bind(wx.EVT_SIZE, self.onResize)

        self.buildEnv()
        self.tracker = TrackingManager(self.frame.map_panel, self.frame.info_grid)
        self.addInitialElements()

    def create_wp(self):
        wp = core.WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(self.pandaPanel.GetClientSize()[0], self.pandaPanel.GetClientSize()[1])
        wp.setParentWindow(self.pandaPanel.GetHandle())
        return wp

    def onResize(self, event):
        self.win.requestProperties(self.create_wp())

    def addInitialElements(self):
        eb = EarthBase()
        eb.model.reparentTo(self.render)
        self.eb = eb

        light = AmbientLight('amb')
        lightNP = self.render.attachNewNode(light)
        self.render.setLight(lightNP)
        self.render.setShaderAuto()

        satellites = [
            SatelliteEntity({'iHead': 00, 'iPitch': 0}, {'dHead': 8, 'dPitch': 3, 'dRoll': 0}, self.frame.map_panel, self.frame.info_grid),
            SatelliteEntity({'iHead': -33, 'iPitch': -65}, {'dHead': -2, 'dPitch': 1, 'dRoll': 0}, self.frame.map_panel, self.frame.info_grid),
            SatelliteEntity({'iHead': 33, 'iPitch': 130}, {'dHead': 1, 'dPitch': -3, 'dRoll': 0}, self.frame.map_panel, self.frame.info_grid)
        ]

        for sat in satellites:
            eb.addChild(sat.anchor)
            self.tracker.track(sat.anchor)

        baseStations = [
            (0, 0),
            (15, -20)
        ]

        for bs in baseStations:
            self.addBaseStation(bs)

        targets = [
            (-50, 14),
            (-90, 88),
        ]

        for t in targets:
            self.addTarget(t)

        self.cam.setPos(0, -100, 0)

    def addTarget(self, latlong):
        targ = TargetPoint(latlong)
        self.eb.addChild(targ)
        self.tracker.addTarget(targ)

    def addBaseStation(self, latlong):
        bs = BaseStation(latlong)
        self.eb.addChild(bs)
        self.tracker.addBaseStation(bs)

    def addSatellite(self, latlong, speed):
        sat = SatelliteEntity(
            {'iHead': latlong[0], 'iPitch': -latlong[1]},
            {'dHead': speed[0], 'dPitch': speed[1], 'dRoll': 0},
            self.frame.map_panel,
            self.frame.info_grid
        )

        self.eb.addChild(sat.anchor)
        self.tracker.track(sat.anchor)

    def buildEnv(self):
        Config.setConfigPath(r'C:\Users\pajab\Documents\MSGIS\GEOG656\Panda3dFinal\config')

        AssetFactory.setLoader(self.loader)
        AssetFactory.setAssetRoot(os.path.abspath(r'C:\Users\pajab\Documents\MSGIS\GEOG656\Panda3dFinal\assets'))

        TaskManager.setTaskManager(self.taskMgr)


core.loadPrcFileData('startup', 'window-type none')

soarApp = SOAR()
soarApp.run()
