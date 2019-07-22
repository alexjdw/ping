import pygame, numpy as np
from OpenGL.GL import *
from ..utils import ReprMixin, vector
from ..pallette import C_WHITE
from random import random, choice
import glm


class Point3D(ReprMixin):
    "A vertex with additional data for color, texture coords, and normals."
    def __init__(self,
                 x, y, z,
                 texcoords=None,
                 normal=None,
                 color=None):
        self.vertex = glm.vec3(x, y, z)
        self.texcoords = texcoords
        self.normal = normal
        self.color = color
        if self.color is None:
            self.color = (.9, .8, .7)
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
        if self.texcoords is not None:
            arr_format += 't'
            self._VBO.extend(self.texcoords)
        if self.normal is not None:
            arr_format += 'n'
            self._VBO.extend(self.normal)
        if self.color is not None:
            arr_format += 'c'
            self._VBO.extend(self.color)
        self._VBO_is_compiled = True
        return arr_format
