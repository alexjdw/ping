from .utils import ReprMixin
from contextlib import contextmanager
from collections import namedtuple
from OpenGL.GL import *
from OpenGL.GL import shaders,\
                      glVertexAttribPointer,\
                      glEnableVertexAttribArray,\
                      glDeleteVertexArrays,\
                      glGetIntegerv,\
                      sizeof, ctypes, GLuint
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, \
                                                  glBindVertexArray

VptrArgs = namedtuple("VptrArgs", "index size typ normalized stride pointer")


class VAO(ReprMixin):
    def __init__(self, locations):
        self.locations = locations
        self.VBOs = []
        self.vptr_args = []

        # VAO index or 'name' in OpenGL
        self._index = GLuint(0)
        glGenVertexArrays(1, self._index)

        # Plan: Store the arguments for a glVertex call,
        # then, when a buffer is added, activate the VBO
        # and call glVertexAttribPointer with stored arguments.
        offset = 0
        count = 0
        stride = 0
        for loc, attribs in self.locations.items():
            if 'vec' in attribs.type:
                size = int(attribs.type[3])
            elif 'mat' in attribs.type:
                size = int(attribs.type[3]) ** 2
            elif 'float' in attribs.type:
                size = 1
            else:
                raise TypeError("Unsupported type for VAO: " + attribs.type)
            self.vptr_args.append(
                [loc,
                 size,
                 GL_FLOAT,
                 GL_FALSE,
                 0,  # mulitply by stride later
                 ctypes.c_void_p(offset)
                 ])
            offset += size * sizeof(ctypes.c_float)
            stride += size
        for arg in self.vptr_args:
            arg[4] = stride * sizeof(ctypes.c_float)

    def add_VBO(self, VBO):
        if not (self._bound):
            raise VAOError("VAO is not currently bound.")

        self.VBOs.append(VBO)
        try:
            VBO.bind()
            for args in self.vptr_args:
                glEnableVertexAttribArray(args[0])
                glVertexAttribPointer(*args)
        finally:
            VBO.unbind()

    def bind(self):
        glBindVertexArray(self._index)
        self._bound = True

    def unbind(self):
        glBindVertexArray(0)
        self._bound = False


class VAOError(Exception):
    pass
