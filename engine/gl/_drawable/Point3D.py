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
        "Old-style drawing compatability. Call after glBegin()."
        glBegin(GL_POINTS)
        if self.color is not None:
            glColor3fv(self.color)
        glVertex3fv(self.vertex)
        glEnd()

    def compile_VBO(self, include_color=True,
                    force_color=False, color=None):
        if include_color:
            if not force_color:
                if self.color is not None and color is None:
                    color = self.color
                else:
                    raise ValueError(f"Tried to render with color, but color wasn't provided. not provided. {repr(self)}")
            self._VBO = np.concatenate((np.array(self.vertex, 'f'), color))
        self._VBO = np.array(self.vertex, 'f')


    def draw(self, target):
        'Draw the point as a single pixel on a 2d target surface.'
        target.fill(self.color, (self.pos, (1,1)))
