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
            offset=None,
            shader=None,
            enable_texture=False,
            enable_normals=False):
        self.shapes = shapes_list
        self.color = color
        self.offset = offset
        self._VBO_is_compiled = False
        self.enable_texture = enable_texture
        self.enable_normals = enable_normals

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

    def compile_VBO(self, include_color=False,
                    force_color=False, color=None):
        '''Compiles the verticies of all faces into a VBO-style nested array.

        :param include_color: includes a color value in the result.
        :param force_color: forces the parent color to apply to the child objects.
          - :include_color: must be set to True, otherwise you won't get a color back.
        :param color: Override the shape's .color value for this call.'''
        vbos = []
        if color is None and include_color:
            color = self.color
        for s in self.shapes:
            s.compile_VBO(include_color, force_color, color=color)
            vbos.append(s._VBO)

        self._VBO = np.concatenate(vbos)
        self._VBO_is_compiled = True

    color = property(get_color, set_color)

    def custom_render(self, with_color=True, override_color=None):
        '''Render with a few more options. Note: always recompiles.'''
        if override_color is None:
            self._compile_VBO(with_color)
        else:
            self._compile_VBO(with_color, override_color)

        return (self._VBO, self.shader, GL_TRIANGLES)

    def render(self):
        '''
        Prepares and returns the VBO-formatted data.

        Returns ([[VBO-ready array of vertexes]], shader, GL_MODE) for drawing.
        '''
        if not self._VBO_is_compiled:
            self.compile_VBO()

        return (self._VBO, self.shader, GL_TRIANGLES)


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
