import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *


class Shape2D(ReprMixin):
    "A 2d polygon made from a collection of points."
    def __init__(self, points_list, color):
        if len(points_list) != 3:
            raise ValueError("A triangle can only accept 3 points. (" + len(points_list) + " received)")
        self.points = points_list
        self.color = color

    def GLDraw(self):
        glColor3fv(self.color)
        for p in self.points:
            glVertex3fv(p.vertex)

    def GLDraw_outline(self):
        glBegin(GL_LINES)
        glVertex3fv(self.points)
        glEnd()
