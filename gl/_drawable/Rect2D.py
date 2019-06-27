from OpenGL.GL import *
from OpenGL.GLU import *
from ..utils import ReprMixin
from random import random

class Rect2D(ReprMixin):
    "A 2d rectangle made from a collection of four points."
    def __init__(self, points_list, color=None):
        self.points = [points_list[0], points_list[1], points_list[3],
                       points_list[0], points_list[3], points_list[2]]
        self.lines = points_list
        if len(points_list) != 4:
            raise AttributeError("to form a square, include four points.")
        self.color = color
        self.color = [random(), random(), random()]

    def GLDraw(self):
        glBegin(GL_TRIANGLES)
        if self.color is not None:
            glColor3fv(self.color)
        for p in self.points:
            glVertex3fv(p.vertex)
        glEnd()

    def GLDraw_outline(self):
        glBegin(GL_LINES)
        glVertex3fv(self.lines)
        glEnd()
