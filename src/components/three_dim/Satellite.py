from panda3d.core import PerspectiveLens, LensNode, TransparencyAttrib, TextureStage, Vec4, Vec3, Vec2

from src.Util.TaskManager import TaskManager
from src.components.three_dim.Entity import Entity


class SatelliteEntity:
    def __init__(self, position, rotation, map_panel, info_panel):
        self.map_panel = map_panel
        self.info_panel = info_panel
        self.satellite = Entity('satellite')
        self.anchor = Entity('anchor')
        self.anchor.addChild(self.satellite)
        self.anchor.rot = rotation
        self.anchor.rot['dPitch'] = -rotation['dPitch']
        self.anchor.pos['heading'] = position['iHead'] + 90
        self.anchor.pos['pitch'] = position['iPitch']

        self.highlight = Entity('highlight')
        self.highlight.model.setTransparency(TransparencyAttrib.MAlpha)
        ts = TextureStage(f'{self.highlight.getUID()}_TS')
        ts.setCombineRgb(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcAlpha)
        ts.setColor(Vec4(1, 1, 0, 0.2))
        self.highlight.model.setTexture(ts, self.highlight.texture)
        self.anchor.addChild(self.highlight)

        self.buildView()

        TaskManager.registerTask(self.anchor.spinConst, f'{self.anchor.getUID()}_SPINNER')

    def buildView(self):
        lens = PerspectiveLens()
        lens.setFar(13)
        lens.setFov(10)
        lensNode = self.anchor.model.attachNewNode(LensNode(f'{self.satellite.getUID()}_LENS'))
        lensNode.node().setLens(lens)
        lensNode.node().showFrustum()
        lensNode.reparentTo(self.anchor.model)
        lensNode.setPos(self.satellite.pos['x'], self.satellite.pos['y'], self.satellite.pos['z'])
        lensNode.lookAt(self.anchor.model)

