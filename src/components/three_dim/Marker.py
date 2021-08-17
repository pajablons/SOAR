from panda3d.core import TransparencyAttrib

from src.components.three_dim.Entity import Entity


# Marker class for all point entities (ie: basestations, targets)
class Marker(Entity):
    def __init__(self, position, tp):
        super().__init__(tp)
        # Establish transparency.  Actual texture aspects are handled in the texture files (1:1 with point types)
        self.model.setTransparency(TransparencyAttrib.MAlpha)

        # Kick to initial position
        self.model.setHpr(position[0] - 90, position[1], 0)
