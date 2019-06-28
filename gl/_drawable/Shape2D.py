import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *
from random import random


class Shape2D(ReprMixin):
    "A 2d polygon made from a collection of points."
    def __init__(self, points_list, color):
        self.points = points_list
        self.color = color
        self.color = [random(), random(), random()]

    def GLDraw(self):
        glBegin(GL_POLYGON)
        if (self.Color is not None):
            glColor3fv(self.color)

        for p in self.points:
            glVertex3fv(p.vertex)
        glEnd()

    def GLDraw_outline(self):
        glBegin(GL_LINES)
        glVertex3fv(self.points)
        glEnd()

    @property
    def VBO_array(self):
        return np.array(self.points)
