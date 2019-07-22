import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *
from random import random


class Shape2D(ReprMixin):
    "A 2d polygon made from a collection of points."
    def __init__(self,
                 points,
                 texcoords=None,
                 normal=None,
                 mode=GL_TRIANGLES,
                 color=None):
        '''
        :param points: A flat list of Point3D objects. Must conform to the
          shape specified by mode, i.e. TRIANGLES must have a len divisible
          by 3, QUADS by 4. Defaults to GL_TRIANGLES.
        :param color: A tuple representing a color. Generally used if there is
          no texture. Applies the color to any points that don't have a color.
        :param texcoords: A list of tuples representing texture coordinates.
        :param normals: A single normal for the face.
        '''
        if mode == GL_TRIANGLES:
            if len(points) % 3:
                raise ValueError(
                        f'''{points} has a non-triangluar number of vertexes.
                        Break your polygons into triangles of len=3,
                        then smoosh them together. Example:\n
                        \t[p1,p2,p3, # first triangle\n
                        \t p4,p5,p6, # second triangle\n
                        \t p7,p8,p9] # third triangle, etc...''')
        elif mode == GL_QUADS:
            if len(points) % 4:
                raise ValueError(
                        f'''{points} has the wrong number of vertexes.
                        Break your polygons into quads of len=4,
                        then smoosh them together. Example:\n
                        \t[p1,p2,p3,p4,  # first quad\n
                        \t p5,p6,p7,p8]  # second quad, etc.''')
        self.mode = mode
        self.points = points

        if color is not None:
            for point in self.points:
                if point.color is None:
                    point.color = color

        self._VBO_is_compiled = False

    def GLDraw(self):
        "Old-style drawing for compatibility. glBegin() before calling."
        if self.color is not None:
            glColor3fv(self.color)
        for p in self.points:
            if p.color is not None:
                glColor3fv(self.color)
            glVertex3fv(p.vertex)

    def GLDraw_outline(self):
        "Old-style drawing for compatibility. glBegin() before calling."
        # TODO
        pass

    def compile_VBO(self, force=False):
        '''
        Saves VBO array containing the vertexes & texture/color
        data for this shape.
        '''
        if self._VBO_is_compiled and not force:
            return

        vbo = []
        arr_format = self.points[0].compile_VBO(force=True)


        for p in self.points:
            p.compile_VBO()
            vbo.append(p._VBO)

        self._VBO = np.array(vbo, 'f')
        self._VBO_is_compiled = True
        return arr_format
