import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from ..utils import ReprMixin
from random import random
from .Shape2D import Shape2D


class Rect2D(Shape2D, ReprMixin):
    "A 2d rectangle made from a collection of four points."
    def __init__(self, points_list, color=None):
        if len(points_list) != 4:
            raise AttributeError("to form a square, include exactly four points.")

        self.points = [points_list[0], points_list[1], points_list[3],
                       points_list[0], points_list[3], points_list[2]]
        self.lines = points_list
        self.color = color

    @property
    def VBO_array(self):
        '''Returns an array of vertex arrays.'''
        return np.array([np.array(p.vertex) for p in self.points])
