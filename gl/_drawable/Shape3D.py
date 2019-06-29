import pygame, numpy as np
from ..utils import ReprMixin
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

from .Point3D import Point3D
from .Rect2D import Rect2D


class Shape3D(ReprMixin):
    "A 3d shape made from a collection of 2d faces."
    def __init__(self, shapes_list, color=(.5, .5, .5, 1.0), shader=None):
        self.shapes = shapes_list
        self.color = color
        if (len(self.color) != 4):
            # Ensure color includes alpha
            self.color = (self.color[0], self.color[1], self.color[2], 1.)
        self._VBO_is_compiled = False
        if shader is None:
            # No shader provided. Fill with color.
            # Create the C code for the vertex shader.
            vshader = shaders.compileShader("""#version 120
            void main() {
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            }""", GL_VERTEX_SHADER)
            # Create the C code for the fragment shader.
            fshader = shaders.compileShader("""#version 120
            void main() {
                gl_FragColor = vec4""" + self.color.__str__() + """;
            }""", GL_FRAGMENT_SHADER)
            # Have openGL compile both shaders and save the result.
            self.shader = shaders.compileProgram(vshader, fshader)
        else:
            # An already-compiled shader was provided.
            self.shader = shader

    def GLDraw(self):
        for s in self.shapes:
            s.GLDraw()

    def GLDraw_outline(self):
        for s in self.shapes:
            s.GLDraw_outline()

    @property
    def VBO_array(self):
        "Returns a numpy array of points."
        vbo = []
        for s in self.shapes:
            vbo.extend(s.VBO_array)

        return np.array(vbo, 'f')

    def to_renderable(self):
        "Returns (VBO array (an array of vertexes), shader, GL_MODE) for drawing."
        if not self._VBO_is_compiled:
            self._VBO = self.VBO_array
            self._VBO_is_compiled = True

        return (self._VBO, self.shader, GL_TRIANGLES)


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
        Rect2D([points[0], points[1], points[2], points[3]], (.1, .8, .8)),
        Rect2D([points[1], points[5], points[3], points[7]], (.1, .9, .1)),
        Rect2D([points[4], points[0], points[6], points[2]], (.3, .4, .5)),
        Rect2D([points[4], points[5], points[0], points[1]], (.1, .1, .9)),
        Rect2D([points[2], points[3], points[6], points[7]], (.5, .5, .5)),
    ]
    return Shape3D(shapes, color)


def cube(length, first_point, color=(0,0,0)):
    'Constructs a cube.'
    return box(length, length, length, first_point, color)


def pyramid(base_len, base_wid, height, first_point, color=(0,0,0)):
    pass
