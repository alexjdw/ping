import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *
from random import random


class Shape2D(ReprMixin):
    '''A 2d polygon made from a collection of points.'''
    def __init__(self, points, color):
        '''
        :param triangles: A flat list of Point3D objects where len(triangles)
          is divisible by 3.
        :param color: A tuple representing a color.
        '''
        if len(triangles) % 3:
            raise ValueError(
                    f'''{points} has a non-triangluar number of vertexes.
                    Break your polygons into triangles of len=3,
                    then smoosh them together. Example:\n
                    \t[p1,p2,p3, # first triangle
                    \t p4,p5,p6, # second triangle
                    \t p7,p8,p9] # third triangle''')

        self.points = []
        self.color = color

    def GLDraw(self):
        "Old-style drawing. Preserved for compatibility. glBegin() before calling."
        if self.color is not None:
            glColor3fv(self.color)
        for p in self.points:
            if p.color is not None:
                glColor3fv(self.color)
            glVertex3fv(p.vertex)

    def GLDraw_outline(self):
        "Old-style drawing. Preserved for compatibility. glBegin() before calling."
        glVertex3fv(self.lines)

    def compile_VBO(self, include_color=True,
                    force_color=False, color=None):
        '''Returns a numpy array containing the vertexes and,
        if requested, the color data for this shape.'''
        # Shapes do not include a full render property
        # and offsets as they are meant to be faces of
        # a 3D object.
        vbo = []
        if color is None and include_color:
            color = self.color
        for p in self.points:
            p.compile_VBO(include_color, force_color, color)
            vbo.append(p._VBO)

        self._VBO = np.array(vbo, 'f')
