'''A home for uncompiled strings of shaders.'''
from importlib import import_module
from OpenGL.GL import shaders
import os


def _pipeflags(flags):
    '''
    Pipes the flags together i.e. GL_FLAG1 | GLFLAG2 | GLFLAG3 etc.

    flags is None -> return 0
    flags is not iterable -> return flags
    flags is iterable -> pipe flags together and return result
    '''
    if hasattr(flags, '__getindex__') or hasattr(flags, '__getindex__'):
        result = 0
        for flag in flags:
            result = result | flag
        return result
    if flags is None:
        return 0
    return flags


def compile(name, GL_FLAGS):
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, '_shaders', name + '.shader')) as f:
            code = f.read()
    except Exception as e:
        raise ValueError(f"'{name}' is not an available shader.", e)
    return shaders.compileShader(code, _pipeflags(GL_FLAGS))


def get_raw_code(name):
    try:
        from ._shaders import name
    except ImportError:
        raise ValueError(f"'{name}' is not an available shader.")
    return name.code
