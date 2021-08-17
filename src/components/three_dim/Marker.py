from panda3d.core import TextureStage, Vec4, TransparencyAttrib, Vec3

from src.components.three_dim.Entity import Entity


class Marker(Entity):
    def __init__(self, position, tp):
        super().__init__(tp)
        self.model.setTransparency(TransparencyAttrib.MAlpha)

        self.model.setHpr(position[0] - 90, position[1], 0)
