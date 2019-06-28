import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from ..utils import ReprMixin
from random import random


class Rect2D(ReprMixin):
    "A 2d rectangle made from a collection of four points."
    def __init__(self, points_list, color=None):
        if len(points_list) != 4:
            raise AttributeError("to form a square, include exactly four points.")

        self.points = [points_list[0], points_list[1], points_list[3],
                       points_list[0], points_list[3], points_list[2]]
        self.lines = points_list
        self.color = color

    def GLDraw(self):
        if self.color is not None:
            glColor3fv(self.color)
        for p in self.points:
            glVertex3fv(p.vertex)
            # print(p.vertex)

    def GLDraw_outline(self):
        glVertex3fv(self.lines)

    @property
    def VBO_array(self):
        return np.array([p.vertex for p in self.points])