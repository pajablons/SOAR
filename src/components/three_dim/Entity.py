from direct.task import Task

from src.Util.AssetFactory import AssetFactory
from src.Util.Config import Config


# Entity parent class.  Effectively a wrapper for panda3d nodepaths
class Entity:
    # Unique id base counter
    id = 0

    # Every entity accepts a config file specifying information such as initial position and display properties
    def __init__(self, config):
        # Establish UID
        self.id = Entity.id
        Entity.id += 1

        # Load our config
        self.conf = Config.getConfig(config)

        # Load 3d assets
        self.model = None
        self.texture = None
        self.loadAssets()

        # Easier access to certain aspects of the configuration
        self.pos = self.conf['position']
        self.scale = self.conf['scale']
        self.rot = self.conf['rotation']

        # TODO: Potentially refactor to a Spinner subclass?
        if 'rotation' in self.conf.keys():
            self.spinRate = self.conf['rotation']

        # Kick to initial position based on config
        self.toInitialPosition()
        self.toInitialHPR()
        self.model.setScale(self.scale['x'], self.scale['y'], self.scale['z'])

    # UID in the form 'ClassName_IDNum', ie 'EarthBase_4'
    def getUID(self) -> str:
        return f'{self.__class__.__name__}_{self.id}'

    # Attach a child entity to a parent.  Wrapper about nodepath's reparentTo connecting models
    def addChild(self, child: 'Entity'):
        child.model.reparentTo(self.model)

    def loadAssets(self):
        self.model = AssetFactory.loadModel(self.conf['assets']['model'])  # Access the model file

        # Access our texture object
        texPath = self.conf['assets']['texture']
        if len(texPath) > 0:
            self.texture = AssetFactory.loadTexture(texPath)
            self.model.setTexture(self.texture)

    # Set position to config settings
    def toInitialPosition(self):
        initialX = self.conf['position']['x']
        initialY = self.conf['position']['y']
        initialZ = self.conf['position']['z']

        self.model.setPos(initialX, initialY, initialZ)

    # Set rotation to config settings
    def toInitialHPR(self):
        initialH = self.conf['position']['heading']
        initialP = self.conf['position']['pitch']
        initialR = self.conf['position']['roll']

        self.model.setHpr(initialH, initialP, initialR)

    # Task management handled by panda3d.  We spin with constant rotational velocity.
    def spinConst(self, task):
        headRate = self.rot['dHead']
        pitchRate = self.rot['dPitch']
        rollRate = self.rot['dRoll']

        deg = task.time % 360

        # [stage in current orbit] * [rate of rotation] + [initial offset] = new rotation
        self.model.setHpr(deg * headRate + self.pos['heading'], deg * pitchRate + self.pos['pitch'], deg * rollRate)

        # Tell panda3d to keep executing the task again and again
        return Task.cont
