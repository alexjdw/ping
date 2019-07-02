'''A home for uncompiled strings of shaders.'''
from importlib import import_module
from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from contextlib import contextmanager
from collections import namedtuple
import os

ShaderVar = namedtuple('ShaderVar', 'cls type name')


class Shader:
    '''
    A shader, compiled from c code. This shader takes a file and
    compiles it. It also parses the c code for `in`, `out`, `uniform`,
    `varying`, `attribute` statements and makes a note of them for validation.

    references:
    https://gamedev.stackexchange.com/questions/29672/in-out-keywords-in-glsl
    https://gamedev.stackexchange.com/questions/29672/in-out-keywords-in-glsl
    '''
    # A dict to avoid recompiling of the same shader.
    compiledShaders = {}

    def __init__(self, file, shadertype, abspath=False):
        '''
        :param file: the filename. if abspath=True, file is the fully qualified
          absolute path.
        :param shadertype: GL_VERTEX_SHADER or GL_FRAGMENT_SHADER
        :abspath: Lets the shader know the file path you're passing in is
          an absolute path.'''
        if file is None:
            return  # allow alternate constructors
        if file in Shader.compiledShaders:
            # If we've already loaded this shader, just copy it
            # and remove the models.
            other = Shader.compiledShaders[file]
            self.__dict__ = other.__dict__.copy()
            self.models = []
            return

        if shadertype not in (GL_VERTEX_SHADER, GL_FRAGMENT_SHADER):
            raise TypeError("Type should be GL_VERTEX or GL_FRAGMENT")
        self.file = file
        self.shadertype = shadertype

        try:
            if abspath:
                fullpath = file
            else:
                here = os.path.dirname(os.path.abspath(__file__))
                fullpath = os.path.join(here, '_shaders', file + '.shader')
            with open(fullpath) as f:
                self._code = f.read()
        except Exception as e:
            raise ValueError(f"'{name}' is not an available shader.", e)

        self.shader = shaders.compileShader(self._code, shadertype)
        self.parse()
        Shader.compiledShaders[file] = self

    @classmethod
    def from_raw_code(cls, code, shadertype):
        '''
        Alternate constructor that allows you to pass in raw C code. Useful
        for testing out different shaders.
        '''
        if shadertype not in (GL_VERTEX_SHADER, GL_FRAGMENT_SHADER):
            raise TypeError("Type should be GL_VERTEX_SHADER or GL_FRAGMENT_SHADER")
        self = cls(None, shadertype)
        self.file = None
        self._code = code
        self.shader = shaders.compileShader(self._code, shadertype)
        self.parse()
        return self

    def parse(self):
        self.vars = []
        vartypes = {'in', 'out', 'inout', 'uniform', 'attribute', 'varying'}
        for line in self._code.split('\n'):
            words = line.split()
            if not len(words):
                continue
            if words[0] in vartypes:
                if words[1] in ('highp', 'mediump', 'lowp'):
                    # Skip the precision
                    self.vars.append(
                        ShaderVar(words[0], words[2], words[3].rstrip(';')))
                else:
                    self.vars.append(
                        ShaderVar(words[0], words[1], words[2].rstrip(';')))


class Pipeline:
    def __init__(self, vertex_shader, fragment_shader):
        self.vert = vertex_shader
        self.frag = fragment_shader
        self.models = []
        self._program = shaders.compileProgram(self.vert.shader, self.frag.shader)

    def add_model(self, model):
        "Add a Shape3D model to be rendered with this shader pair."
        self.models.append(model)

    @contextmanager
    def rendering(self):
        shaders.glUseProgram(self._program)
        yield
        shaders.glUseProgram(0)
