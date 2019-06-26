import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *


class Shape3D(ReprMixin):
    "A 2d polygon made from a collection of points."
    def __init__(self, points_list, color):
        self.points = points_list
        self.color = color

    # def get_momentum(self):
    #     return sqrt(self.vector[0] ** 2 + self.vector[1] ** 2 + self.vector[2] ** 2)

    # def set_momentum(self, val):
    #     vsum = abs(self.vector[0]) + abs(self.vector[1]) + abs(self.vector[2])
    #     if (vsum):
    #         scalar = val / vsum
    #         self.vector = self.vector * [scalar]

    #     else:
    #         self.vector = np.array([0., 0., 0.])

    # momentum = property(get_momentum, set_momentum)

    def GLDraw(self):
        glBegin(GL_POLYGON)
        glColor3fv(self.color)
        for p in self.points:
            glVertex3fv(p.vertex)
        glEnd()

    def GLDraw_outline(self):
        glBegin(GL_LINES)
        glVertex3fv(self.points)
        glEnd()
