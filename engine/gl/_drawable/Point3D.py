import pygame, numpy as np
from OpenGL.GL import *
from ..utils import ReprMixin, vector
from ..pallette import C_WHITE
from random import random, choice

RANDO_COLORS = True
rando_choices = [.1, .6]
class Point3D(ReprMixin):
    "A vertex with additional data for color, texture coords, and normals."
    def __init__(self,
                 x, y, z,
                 texcoords=None,
                 normal=None,
                 color=None):
        self.vertex = (x, y, z)
        self.texcoords = texcoords
        self.normal = normal
        self.color = color
        if self.color is None and RANDO_COLORS:
            self.color = (random() / 3 + .6, random() / 3 + .6, random() / 3 + .6)
        self._VBO_is_compiled = False

    def GLDraw(self):
        "Old-style drawing compatability. Call after glBegin()."
        glBegin(GL_POINTS)
        if self.color is not None:
            glColor3fv(self.color)
        glVertex3fv(self.vertex)
        glEnd()

    def compile_VBO(self, force=False):
        '''
        Compiles the point to VBO format (a flat array), then returns
        the ordering/format of the array in string form. Data that's not
        present is omitted, so a return val of 'vt' means only vertex and
        texture coords are included.
        '''
        if self._VBO_is_compiled and not force:
            return
        self._VBO = list(self.vertex)
        arr_format = 'v'
        if self.texcoords:
            arr_format += 't'
            self._VBO.extend(self.texcoords)
        if self.normal:
            arr_format += 'n'
            self._VBO.extend(self.normal)
        if self.color:
            arr_format += 'c'
            self._VBO.extend(self.color)
        self._VBO_is_compiled = True
        return arr_format
