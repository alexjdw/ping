import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from .Point3D import Point3D
from .Rect2D import Rect2D
import ..shader_presets

class Shape3D(ReprMixin):
    "A 3d shape made from a collection of 2d faces."
    def __init__(self, shapes_list, color=None, offset=None, shader=None):
        self.shapes = shapes_list
        self.color = color
        self.offset = offset
        self._VBO_is_compiled = False
        if shader is None:
            # No shader provided. Fill with color.
            # Create the C code for the vertex shader.
            vshader = shader_presets.compile('vertex_default', GL_VERTEX_SHADER)
            # Create the C code for the fragment shader.
            fshader = shader_presets.compile('fragment_default', GL_FRAGMENT_SHADER)
            # Have openGL compile both shaders and save the result.
            self.shader = shaders.compileProgram(vshader, fshader)
        else:
            # An already-compiled shader was provided.
            self.shader = shader

    def GLDraw(self):
        "Draws the shape. Old-style drawing mechanism. Deprecated."
        for s in self.shapes:
            s.GLDraw()

    def GLDraw_outline(self):
        "Old-style drawing mechanism. Draws the shape."
        for s in self.shapes:
            s.GLDraw_outline()

    def compile_VBO(self, include_color=True,
                    force_color=False, color=None):
        "Compiles the verticies of all faces into a VBO-style nested array."
        vbo = []
        if color is None:
            color = self.color
        for s in self.shapes:
            s.compile_VBO(include_color=False, override_color=False, color=color)
            vbo.extend(s._VBO)

        self._VBO = np.array(vbo, 'f')
        self._VBO_is_compiled = True

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        self._VBO_is_compiled

    color = property(get_color, set_color)
    offset = property(get_offset, set_offset)

    def custom_renderable(self, with_color=True):
        if not self._VBO_is_compiled:
            self._compile_VBO(with_color)
        return (self._VBO, self.shader, GL_TRIANGLES)

    def render(self):
        '''
        Prepares the internal data to render the function.

        Returns ([[VBO-ready array of vertexes]], shader, GL_MODE) for drawing.
        '''
        color, offset = False, False
        if self.color is not None:
            color = True
        if self.offset is not None:
            offset = True

        return self.custom_renderable(offset, color)


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
        Rect2D([points[0], points[1], points[2], points[3]], (.1, .8, .8)),
        Rect2D([points[1], points[5], points[3], points[7]], (.1, .9, .1)),
        Rect2D([points[4], points[0], points[6], points[2]], (.3, .4, .5)),
        Rect2D([points[4], points[5], points[0], points[1]], (.1, .1, .9)),
        Rect2D([points[2], points[3], points[6], points[7]], (.5, .5, .5)),
        Rect2D([points[5], points[4], points[7], points[6]], (.1, .5, .9)),
    ]
    return Shape3D(shapes, color)


def cube(length, first_point, color=(0, 0, 0)):
    'Constructs a cube.'
    return box(length, length, length, first_point, color)


def pyramid(base_len, base_wid, height, first_point, color=(0, 0, 0)):
    pass
