from direct.interval.MetaInterval import Sequence
from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from math import pi, sin, cos
from panda3d.core import MeshDrawer2D, Filename, AmbientLight, Spotlight, PerspectiveLens, TextureAttrib, \
    TransparencyAttrib, TextureStage, LensNode, NodePath, SamplerState, GraphicsStateGuardian, Texture, \
    DirectionalLight, Vec4

from panda3d.core import Point3


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.sphere = self.loader.loadModel('assets/earth.bam')
        self.sphere.reparentTo(self.render)
        self.sphere.setPos(0, 0, 0)

        tex = self.loader.loadTexture('assets/Highlight.png')
        ts = TextureStage('ts')
        ts.setColor(Vec4(0, 1, 1, 0.2))
        ts.setCombineRgb(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcAlpha)

        tex2 = self.loader.loadTexture('assets/Highlight.png')
        ts2 = TextureStage('ts2')
        ts2.setColor(Vec4(1, 0, 1, 0.2))
        ts2.setCombineRgb(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts2.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcAlpha)

        self.tracker = self.loader.loadModel('assets/invisisphere.bam')
        self.tracker.reparentTo(self.sphere)

        self.tracker2 = self.loader.loadModel('assets/invisisphere.bam')
        self.tracker2.reparentTo(self.sphere)

        self.outer = self.loader.loadModel('assets/invisisphere.bam')
        self.outer.reparentTo(self.tracker)
        self.outer.setPos(0, -12, 0)
        self.outer.setScale(0.5, 0.5, 0.5)
        self.outer.setTexture(ts, tex)

        self.outer2 = self.loader.loadModel('assets/invisisphere.bam')
        self.outer2.reparentTo(self.tracker2)
        self.outer2.setPos(0, -12, 0)
        self.outer2.setScale(0.5, 0.5, 0.5)
        self.outer2.setTexture(ts2, tex2)

        self.outer.setTransparency(TransparencyAttrib.MAlpha)
        self.outer2.setTransparency(TransparencyAttrib.MAlpha)

        self.lightSource = self.loader.loadModel('models/camera')
        self.lightSource.reparentTo(self.tracker)
        self.lightSource.setPos(0, -25, 0)

        self.parent2 = self.loader.loadModel('models/camera')
        self.parent2.reparentTo(self.tracker2)
        self.parent2.setPos(0, -25, 0)

        self.cam.setPos(0, -100, 0)

        lens = PerspectiveLens()
        lens.setFar(13)
        proj = self.sphere.attachNewNode(LensNode('proj'))
        proj.node().setLens(lens)
        proj.reparentTo(self.tracker)
        proj.node().showFrustum()
        proj.setPos(0, -25, 0)
        proj.lookAt(self.tracker)

        lens2 = PerspectiveLens()
        lens2.setFar(13)
        proj2 = self.sphere.attachNewNode(LensNode('proj'))
        proj2.node().setLens(lens2)
        proj2.reparentTo(self.tracker2)
        proj2.node().showFrustum()
        proj2.setPos(0, -25, 0)
        proj2.lookAt(self.tracker2)

    def spinCameraTask(self, task):
        angleDeg = (task.time * 5) % 360
        self.sphere.setHpr(-angleDeg, 0, 0)
        self.tracker.setHpr(2*angleDeg, 0, 0)
        self.tracker2.setHpr(-angleDeg, angleDeg, 0)
        return Task.cont


app = MyApp()
app.run()