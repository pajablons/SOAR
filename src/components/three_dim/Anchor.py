from src.components.three_dim.Entity import Entity


# Invisible anchor entity for other entities to move relative to
class Anchor(Entity):
    def __init__(self):
        super().__init__('anchor')

