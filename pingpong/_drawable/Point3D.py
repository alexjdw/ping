import pygame, numpy as np
from ..utils import ReprMixin, vector
from ..pallette import C_WHITE


class Point3D(ReprMixin):
    '''A point requires a relative parent surface. The point will be
    drawn relative to the center (width / 2, height / 2) of the surface.'''
    def __init__(self, parent, x, y, z, color=C_WHITE):
        self.pos3d = np.array([x, y, z])
        self.parent = parent
        self.color = color

    @property
    def pos(self):
        'The relative position of an point when applied to a 2d screen.'
        source = np.array([self.parent.get_width() / 2,
                           self.parent.get_height() / 2,
                           0])
        shrink = vector.dist(self.pos3d, source)

        adjust = (source[:2] - self.pos3d[:2]) / shrink
        pos = self.pos3d[:2] - adjust

        return pos.astype(int)

    def move(self):
        self.pos3d = self.pos3d + self.vector

    def draw(self, target):
        'Draw the point as a single pixel on a 2d target surface.'
        target.fill(self.color, (self.pos, (1,1)))
