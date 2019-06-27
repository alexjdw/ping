import pygame, numpy as np
from OpenGL.GL import *
from ..utils import ReprMixin, vector
from ..pallette import C_WHITE


class Point3D(ReprMixin):
    "A drawable vertex with a color."

    def __init__(self, x, y, z, color=None):
        self.vertex = (x, y, z)
        self.color = color

    def GLDraw(self):
        glBegin(GL_POINTS)
        if self.color is not None:
            glColor3fv(self.color)
        glVertex3fv(self.vertex)
        glEnd()

    def GLDrawC(self):
        glBegin(GL_POINTS)
        glColor3fv(self.color)
        glVertex3fv(self.vertex)
        glEnd()

    # @property
    # def pos(self):
    #     'The relative position of an point when applied to a 2d screen.'
    #     source = np.array([self.parent.get_width() / 2,
    #                        self.parent.get_height() / 2,
    #                        -50])
    #     shrink = vector.dist(self.pos3d, source)

    #     adjust = (source[:2] - self.pos3d[:2]) / shrink
    #     pos = self.pos3d[:2] - adjust

    #     return pos.astype(int)

    # def move(self):
    #     self.pos3d = self.pos3d + self.vector

    def draw(self, target):
        'Draw the point as a single pixel on a 2d target surface.'
        target.fill(self.color, (self.pos, (1,1)))
