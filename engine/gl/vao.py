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
        self.VBOs = set()
        self.vptr_args = []
        self._index = GLuint(0)
        glGenVertexArrays(1, self._index)

        offset = 0
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
                VptrArgs(loc, size, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(offset))
            )
            offset += size * sizeof(ctypes.c_float)

    def add_VBO(self, VBO):
        if not (self._bound):
            raise ValueError("VAO is not currently bound.")

        self.VBOs.add(VBO)
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
