'''A home for uncompiled strings of shaders.'''
from importlib import import_module
from .vao import VAO
from OpenGL.GL import *
from OpenGL.GL import shaders,\
    GL_VERTEX_SHADER,\
    GL_FRAGMENT_SHADER,\
    glGetUniformLocation,\
    glGetAttribLocation
from contextlib import contextmanager
from collections import namedtuple
import os

ShaderVar = namedtuple('ShaderVar', 'cls type name')
# UNI_FUNCS = {
#     "mat4": glUniformMatrix4fv,
#     "mat3": glUniformMatrix3fv,
#     "mat2": glUniformMatrix2fv,
#     "vec4": glUniform4fv,
#     "vec3": glUniform3fv,
#     "vec2": glUniform2fv,
#     "float": glUniform1f
# }


class Shader:
    '''
    A shader, compiled from c code. This shader takes a file and
    compiles it. It also parses the c code for `in`, `out`, `uniform`,
    `varying`, `attribute` statements and makes a note of them for validation.

    references:
    https://gamedev.stackexchange.com/questions/29672/in-out-keywords-in-glsl
    https://gamedev.stackexchange.com/questions/29672/in-out-keywords-in-glsl
    '''
    # Store compiled shaders in a dict to avoid recompiling of the same shader.
    compiledShaders = {}

    def __init__(self, file, shadertype, abspath=False):
        '''
        :param file: the filename. if abspath=True, file is the fully qualified
          absolute path.
        :param shadertype: GL_VERTEX_SHADER or GL_FRAGMENT_SHADER
        :abspath: Lets the shader know the file path you're passing in is
          an absolute path.
        '''
        if file is None:
            return  # allow alternate constructors
        if file in Shader.compiledShaders:
            # If we've already loaded this shader, just copy it
            # and remove the models.
            other = Shader.compiledShaders[file]
            self.__dict__ = other.__dict__.copy()
            # TODO - avoid using copy here.
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
        for quickly testing out different shaders.
        '''
        if shadertype not in (GL_VERTEX_SHADER, GL_FRAGMENT_SHADER):
            raise TypeError("Type should be GL_VERTEX_SHADER or GL_FRAGMENT_SHADER")
        self = cls(None, shadertype)
        self.file = None
        self._code = code
        self.VAO_locs = None
        self.shader = shaders.compileShader(self._code, shadertype)
        self.parse()
        return self

    def parse(self):
        self.vars = []
        locations = {}
        vartypes = {'in', 'out', 'inout', 'uniform', 'attribute', 'varying'}
        for line in self._code.split('\n'):
            line = line.strip()
            words = line.split()
            is_layout = False
            if not len(words):
                continue
            if words[0] == 'layout':
                # example: layout (location=0) in vec4 potato;
                layout, vars = line.split(')')
                words = vars.split()
                if 'location' in layout:
                    loc = int(layout.split('=')[1].strip())
                    is_layout = True

            if words[0] in vartypes:
                if is_layout:
                    if words[1] in ('highp', 'mediump', 'lowp'):
                        # Skip the precision
                        locations[loc] =\
                            ShaderVar(words[0], words[2], words[3].rstrip(';'))
                    else:
                        locations[loc] =\
                            ShaderVar(words[0], words[1], words[2].rstrip(';'))
                else:
                    if words[1] in ('highp', 'mediump', 'lowp'):
                        # Skip the precision
                        self.vars.append(
                            ShaderVar(words[0], words[2], words[3].rstrip(';')))
                    else:
                        self.vars.append(
                            ShaderVar(words[0], words[1], words[2].rstrip(';')))
        if len(locations.keys()) and self.shadertype == GL_VERTEX_SHADER:
            self.VAO_locations = locations


class Pipeline:
    def __init__(self, vertex_shader, fragment_shader):
        self.vert = vertex_shader
        self.frag = fragment_shader
        self._models_and_VAOs = []
        self._program = shaders.compileProgram(self.vert.shader, self.frag.shader)
        self.VAOs = []

        # get uniform locations
        self.uniforms = {}
        self.ins = {}
        for var in self.vert.vars:
            if var.cls == "uniform":
                loc = glGetUniformLocation(self._program, var.name)
                if loc == -1:
                    print("WARNING: Uniform " + var.name + " returned -1; this indicates that the var is not being used by the program.")
                else:
                    self.uniforms[var.name] = (loc, var.type)
            if var.cls == "in" or var.cls == "inout" or var.cls == "varying":
                loc = glGetAttribLocation(self._program, var.name)
                if loc == -1:
                    print("WARNING: Attribute " + var.name + " returned -1; this indicates that the var is not being used by the program.")
                self.ins[var.name] = (loc, var.type)

        for var in self.frag.vars:
            if var.cls == "uniform" and var.name not in self.uniforms:
                loc = glGetUniformLocation(self._program, var.name)
                if loc == -1:
                    print("WARNING: Attribute " + var.name + " location returned -1; this indicates that the var is not being used by the program.")
                self.uniforms[var.name] = [loc, var.type]

    def add_model(self, model):
        "Add a Shape3D model to be rendered with this shader pair."
        try:
            newVAO = VAO(self.vert.VAO_locations)
            newVAO.bind()
            newVAO.add_VBO(model.render_data[0])
        except Exception as e:
            print(e)
        finally:
            newVAO.unbind()
        self._models_and_VAOs.append((model, newVAO))

    @contextmanager
    def rendering(self):
        shaders.glUseProgram(self._program)
        yield
        shaders.glUseProgram(0)
