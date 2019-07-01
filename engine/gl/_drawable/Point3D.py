import pygame, numpy as np
from OpenGL.GL import *
from ..utils import ReprMixin, vector
from ..pallette import C_WHITE


class Point3D(ReprMixin):
    "A vertex with additional spots for color, texture coords, and normals."

    def __init__(self,
                 x, y, z,
                 texcoords=None,
                 normals=None,
                 color=None):
        self.vertex = (x, y, z)
        self.color = color

    def GLDraw(self):
        "Old-style drawing compatability. Call after glBegin()."
        glBegin(GL_POINTS)
        if self.color is not None:
            glColor3fv(self.color)
        glVertex3fv(self.vertex)
        glEnd()

    def compile_VBO(self, force=False):
        if not self._VBO_is_compiled and not force:
            self._VBO = self.vertex
            if self.texcoords:
                self._VBO.extend(self.texcoords)
            if self.normal:
                self._VBO.extend(self.normal)
            if self.color:
                self._VBO.extend(self.color)
            self._VBO_is_compiled = True
            # Note; we are not compiling to numpy here because
            # it complicates the code a bit; numpy.append doesn't
            # work in the same way that [].append works.
