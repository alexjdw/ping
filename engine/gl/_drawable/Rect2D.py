import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from ..utils import ReprMixin
from random import random
from .Shape2D import Shape2D


class Rect2D(Shape2D):
    "A 2d rectangle made from a collection of four points."
    def __init__(self,
                 points,
                 texcoords=None,
                 normals=None,
                 color=None):
        if len(points) != 4:
            raise AttributeError(
                f"{points} can't make a rectangle. Please include\
                    exactly four points.")

        # convert rect to triangles
        self.points = [points[0], points[1], points[3],
                       points[0], points[3], points[2]]
        self.mode = GL_TRIANGLES
        if color is not None:
            for point in self.points:
                if point.color is None:
                    point.color = color

        self._VBO_is_compiled = False
