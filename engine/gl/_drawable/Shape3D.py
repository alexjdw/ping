import pygame, numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.arrays.vbo import VBO
from .Point3D import Point3D
from .Rect2D import Rect2D
from .. import shader_presets
from ..utils import ReprMixin


class Shape3D(ReprMixin):
    "A 3d shape made from a collection of 2d faces."
    def __init__(self,
                 shapes_list, 
                 color=None,
                 mode=GL_TRIANGLES,
                 offset=None):
        '''
        Builds a 3D shape from the given shape list with the given arguments.
        
        :param shapes_list: The faces of the shape.
        :param color: Applies a color to any vertex with no color data.
        :param mode: GL drawing mode constant, normally GL_TRIANGLES.
        :param offset: (x, y, z) offset in 3D space.
        '''
        self.shapes = shapes_list
        if color is not None:
            for s in self.shapes:
                for p in s.points:
                    if p.color is None:
                        p.color = color
        self.offset = offset
        self.mode = mode
        self._VBO_is_compiled = False
        self._VBO_contexts = []
        self._clientstates = []

    def GLDraw(self):
        "Draws the shape. Old-style drawing mechanism. Deprecated."
        for s in self.shapes:
            s.GLDraw()

    def GLDraw_outline(self):
        "Old-style drawing mechanism. Draws the outline. Deprecated."
        for s in self.shapes:
            s.GLDraw_outline()

    def compile_VBO(self, force=False):
        "Compiles the verticies of all faces into a VBO and saves the ref."
        if self._VBO_is_compiled and not force:
            return
        vbos = []
        try:
            self._VBO_format = self.shapes[0].compile_VBO(force=True)
        except IndexError:
            raise ValueError("Shape3D tried to compile to VBO, but it didn't\
                              have any shapes.")
        for s in self.shapes:
            fmt = s.compile_VBO()
            if fmt != self._VBO_format and fmt is not None:
                # TODO figure out a good way of filling in the blanks?
                raise ValueError("While compiling a Shape3D to VBO, a Shape2D\
                    format mismatched with the format for the other shapes.")
            vbos.append(s._VBO)

        self._VBO = VBO(np.concatenate(vbos))
        self._VBO_is_compiled = True

    @property
    def render_data(self):
        if not self._VBO_is_compiled:
            self.compile_VBO()
        return (self._VBO, self.mode, self.offset)

    def rendering(self):
        "Set up the rendering environment."
        byte_offset = 0  # adjusts the pointer by n bytes
        self._clientstates = []
        if 'v' in self._VBO_format:
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 24, self._VBO)
            byte_offset += 12
            self._clientstates.append(GL_VERTEX_ARRAY)

        if 't' in self._VBO_format:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glTexCoordPointer(3, GL_FLOAT, 24, self._VBO + byte_offset)
            byte_offset += 12
            self._clientstates.append(GL_TEXTURE_COORD_ARRAY)

        if 'n' in self._VBO_format:
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(3, GL_FLOAT, 24, self._VBO + byte_offset)
            byte_offset += 12
            self._clientstates.append(GL_NORMAL_ARRAY)

        if 'c' in self._VBO_format:
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(3, GL_FLOAT, 24, self._VBO + byte_offset)
            byte_offset += 12
            self._clientstates.append(GL_COLOR_ARRAY)
        
    def stop_rendering(self):
        "Tear down the rendering environment."
        for state in self._clientstates:
            glDisableClientState(state)
        self._clientstates = []

    def destroy_buffers(self):
        if hasattr(self, '_VBO'):
            del self._VBO
        self.stop_rendering()

    def __del__(self):
        self.destroy_buffers()


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

def cube(length, first_point, color=None):
    'Constructs a cube.'
    return box(length, length, length, first_point, color)


def pyramid(base_len, base_wid, height, first_point, color=None):
    pass
