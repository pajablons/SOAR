from panda3d.core import PerspectiveLens, LensNode, TransparencyAttrib, TextureStage, Vec4, Vec3, Vec2

from src.Util.TaskManager import TaskManager
from src.components.three_dim.Entity import Entity


# Satellite entities encompass three elements:
# - The anchor, assumed to be at the center of the earth
# - The highlight, moving over the surface of the earth
# - The satellite, really a lens showing the coverage cone from the satellite point
class SatelliteEntity:
    def __init__(self, position, rotation):
        # Load up all the component entities
        self.satellite = Entity('satellite')
        self.anchor = Entity('anchor')
        self.anchor.addChild(self.satellite)
        self.anchor.rot = rotation
        # Adjust our inputs to match the earth's model
        self.anchor.rot['dPitch'] = -rotation['dPitch']
        self.anchor.pos['heading'] = position['iHead'] + 90
        self.anchor.pos['pitch'] = position['iPitch']
        # Kick to the initial position (overriding the configs)
        self.anchor.model.setHpr(self.anchor.pos['heading'], self.anchor.pos['pitch'], 0)

        self.highlight = Entity('highlight')

        # Set visual aspects
        self.highlight.model.setTransparency(TransparencyAttrib.MAlpha)
        ts = TextureStage(f'{self.highlight.getUID()}_TS')
        ts.setCombineRgb(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcAlpha)
        ts.setColor(Vec4(1, 1, 0, 0.2))
        self.highlight.model.setTexture(ts, self.highlight.texture)
        self.anchor.addChild(self.highlight)

        # Build the lens
        self.buildView()

        # Trigger constant rate spinning
        TaskManager.registerTask(self.anchor.spinConst, f'{self.anchor.getUID()}_SPINNER')

    # Build the lens
    def buildView(self):
        lens = PerspectiveLens()
        # Set range for the lens display
        lens.setFar(13)
        lens.setFov(10)
        lensNode = self.anchor.model.attachNewNode(LensNode(f'{self.satellite.getUID()}_LENS'))
        lensNode.node().setLens(lens)
        # Make the lens visible
        lensNode.node().showFrustum()
        lensNode.reparentTo(self.anchor.model)
        lensNode.setPos(self.satellite.pos['x'], self.satellite.pos['y'], self.satellite.pos['z'])
        # Orient towards the center of the earth
        lensNode.lookAt(self.anchor.model)

