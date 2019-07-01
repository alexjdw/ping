import pygame, numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from .Point3D import Point3D
from .Rect2D import Rect2D
from .. import shader_presets
from ..utils import ReprMixin


class Shape3D(ReprMixin):
    "A 3d shape made from a collection of 2d faces."
    def __init__(self, shapes_list, 
            color=None,
            offset=None):
        self.shapes = shapes_list
        self.color = color
        self.offset = offset
        self._VBO_is_compiled = False

    def GLDraw(self):
        "Draws the shape. Old-style drawing mechanism. Deprecated."
        for s in self.shapes:
            s.GLDraw()

    def GLDraw_outline(self):
        "Old-style drawing mechanism. Draws the outline. Deprecated."
        for s in self.shapes:
            s.GLDraw_outline()

    def compile_VBO(self, include_color=False,
                    force_color=False, color=None):
        '''Compiles the verticies of all faces into a VBO.'''
        vbos = []
        if color is None and include_color:
            color = self.color
        for s in self.shapes:
            s.compile_VBO(include_color, force_color, color=color)
            vbos.append(s._VBO)

        self._VBO = np.concatenate(vbos)
        self._VBO_is_compiled = True


# Alternate constructors
def box(height, width, depth, first_point, color=None):
    'Constructs a rectangular box.'
    h = np.array([height, 0, 0])
    w = np.array([0, width, 0])
    d = np.array([0, 0, depth])
    p1 = np.array(first_point.vertex)
    points = [np.array(p1),
              np.array(p1 + w),
              np.array(p1 + h),
              np.array(p1 + w + h),
              np.array(p1 + d),
              np.array(p1 + d + w),
              np.array(p1 + d + h),
              np.array(p1 + d + h + w)]

    for index, point in enumerate(points):
        points[index] = Point3D(point[0], point[1], point[2], color)

    shapes = [
        Rect2D([points[0], points[1], points[2], points[3]]),
        Rect2D([points[1], points[5], points[3], points[7]]),
        Rect2D([points[4], points[0], points[6], points[2]]),
        Rect2D([points[4], points[5], points[0], points[1]]),
        Rect2D([points[2], points[3], points[6], points[7]]),
        Rect2D([points[5], points[4], points[7], points[6]]),
    ]

    return Shape3D(shapes, color)

def cube(length, first_point, color=(0, 0, 0)):
    'Constructs a cube.'
    return box(length, length, length, first_point, color)


def pyramid(base_len, base_wid, height, first_point, color=(0, 0, 0)):
    pass
