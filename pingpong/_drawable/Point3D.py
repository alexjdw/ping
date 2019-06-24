import numpy as np
from ..utils import ReprMixin


class Point3D(ReprMixin):
    '''A point requires a relative parent surface. The point will be
    drawn relative to the center (width / 2, height / 2) of the surface.'''
    def __init__(self, parent, x, y, z):
        self.pos3d = np.array([x, y, z])
        self.parent = parent

    @property
    def pos(self):
        scale = self.pos3d[2] ** .33
        return (int(self.pos3d[0] * scale), int(self.pos3d[1] * scale))

    def move(self):
        self.pos3d = self.pos3d + self.vector

    def draw(self):
        "Draw the point as a single pixel"
        Z = self.Z()
        pygame.gfxdraw.box(target,
                pygame.Rect(self.pos, (self.width, self.height),
                self.color))