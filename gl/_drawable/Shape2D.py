import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *
from random import random


class Shape2D(ReprMixin):
    "A 2d polygon made from a collection of points."
    def __init__(self, triangles, color):
        self.points = []
        for t in triangles:
            if len(t != 3):
                raise ValueError(
                    f'''{t} is not a triangle.
                    Break your polygons into tuples of len=3 before
                    creating a new shape.''')
            for p in t:
                self.points.append(p)
        self.color = color

    def GLDraw(self):
        "Old-style drawing. Preserved for compatibility."
        if self.color is not None:
            glColor3fv(self.color)
        for p in self.points:
            if p.color is not None:
                glColor3fv(self.color)
            glVertex3fv(p.vertex)

    def GLDraw_outline(self):
        "Old-style drawing. Preserved for compatibility."
        glVertex3fv(self.lines)

    def compile_VBO(self, include_color=True,
                    force_color=False, color=None):
        "Compiles the verticies of all faces into a VBO-style nested array."
        vbo = []
        if color is None:
            color = self.color
        for s in self.shapes:
            s.compile_VBO(include_color=False, override_color=False, color=color)
            vbo.extend(s._VBO)

        self._VBO = np.array(vbo, 'f')
        self._VBO_is_compiled = True

    @property
    def VBO_array(self):
        return np.array(self.points)
