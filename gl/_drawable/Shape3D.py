import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *

from .Point3D import Point3D
from .Rect2D import Rect2D


class Shape3D(ReprMixin):
    "A 3d shape made from a collection of 2d faces."
    def __init__(self, shapes_list, color):
        self.shapes = shapes_list
        self.color = color

    def GLDraw(self):
        for s in self.shapes:
            s.GLDraw()

    def GLDraw_outline(self):
        for s in self.shapes:
            s.GLDraw_outline()

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

    print(points)
    for index, point in enumerate(points):
        points[index] = Point3D(point[0], point[1], point[2], color)

    shapes = [
        Rect2D([points[0], points[1], points[3], points[2]]),
        Rect2D([points[5], points[4], points[6], points[7]]),
        Rect2D([points[4], points[0], points[2], points[6]]),
        Rect2D([points[4], points[5], points[1], points[0]]),
        Rect2D([points[1], points[5], points[7], points[3]]),
        Rect2D([points[2], points[3], points[7], points[6]]),
    ]
    return Shape3D(shapes, color)

def cube(length, first_point, color=(0,0,0)):
    'Constructs a cube.'
    return box(length, length, length, first_point, color)


def pyramid(base_len, base_wid, height, first_point, color=(0,0,0)):
    pass
