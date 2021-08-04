from direct.task import Task

from src.Util.AssetFactory import AssetFactory
from src.Util.Config import Config


class Entity:
    id = 0

    def __init__(self, config):
        self.id = Entity.id
        Entity.id += 1

        self.conf = Config.getConfig(config)

        self.model = None
        self.texture = None
        self.loadAssets()

        self.pos = self.conf['position']
        self.scale = self.conf['scale']
        self.rot = self.conf['rotation']

        # TODO: Potentially refactor to a Spinner subclass?
        if 'rotation' in self.conf.keys():
            self.spinRate = self.conf['rotation']

        self.toInitialPosition()
        self.toInitialHPR()
        self.model.setScale(self.scale['x'], self.scale['y'], self.scale['z'])

    def getUID(self) -> str:
        return f'{self.__class__.__name__}_{self.id}'

    def addChild(self, child: 'Entity'):
        child.model.reparentTo(self.model)

    def loadAssets(self):
        self.model = AssetFactory.loadModel(self.conf['assets']['model'])

        texPath = self.conf['assets']['texture']
        if len(texPath) > 0:
            self.texture = AssetFactory.loadTexture(texPath)
            self.model.setTexture(self.texture)

    def toInitialPosition(self):
        initialX = self.conf['position']['x']
        initialY = self.conf['position']['y']
        initialZ = self.conf['position']['z']

        self.model.setPos(initialX, initialY, initialZ)

    def toInitialHPR(self):
        initialH = self.conf['position']['heading']
        initialP = self.conf['position']['pitch']
        initialR = self.conf['position']['roll']

        self.model.setHpr(initialH, initialP, initialR)

    def spinConst(self, task):
        headRate = self.rot['dHead']
        pitchRate = self.rot['dPitch']
        rollRate = self.rot['dRoll']

        deg = task.time % 360

        self.model.setHpr(deg * headRate, deg * pitchRate, deg * rollRate)

        return Task.cont
