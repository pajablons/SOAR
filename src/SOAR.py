from direct.showbase.ShowBase import ShowBase
import os

from src.Util.AssetFactory import AssetFactory
from src.Util.Config import Config
from src.Util.TaskManager import TaskManager
from src.components.EarthBase import EarthBase
from src.components.Satellite import SatelliteEntity


class SOAR(ShowBase):
    def __init__(self):
        super().__init__()
        self.buildEnv()

        eb = EarthBase()
        eb.model.reparentTo(self.render)

        satellites = [
            SatelliteEntity({'dHead': 3, 'dPitch': 3, 'dRoll': 0}),
            SatelliteEntity({'dHead': -2, 'dPitch': 1, 'dRoll': 0}),
            SatelliteEntity({'dHead': 1, 'dPitch': -3, 'dRoll': 0})
        ]

        for sat in satellites:
            eb.addChild(sat.anchor)

        self.cam.setPos(0, -100, 0)

    def buildEnv(self):
        Config.setConfigPath(os.path.abspath('../config/'))

        AssetFactory.setLoader(self.loader)
        AssetFactory.setAssetRoot(os.path.abspath('../assets/'))

        TaskManager.setTaskManager(self.taskMgr)


soarApp = SOAR()
soarApp.run()
