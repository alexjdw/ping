'''A home for uncompiled strings of shaders.'''
from OpenGL.GL import shaders


def _pipeflags(flags_iterable):
    '''
    Pipes the flags together i.e. GL_FLAG1 | GLFLAG2 | GLFLAG3 etc.

    flags is None -> return 0
    flags is not iterable -> return flags
    flags is iterable -> pipe flags together and return result
    '''
    if hasattr(flags, '__getindex__') or hasattr(flags, '__getindex__'):
        result = 0
        for flag in flags_iterable:
            result = result | flag
        return result
    if flags is None:
        return 0
    return flags

def compile(name: String, GL_FLAGS: Any):
    try:
        getattr(__import__('._shaders', fromlist=[name]), name)
    except ImportError:
        raise ValueError(f"'{name}' is not an available shader.")
    return shaders.compileShader(name.code, _pipeflags(GL_FLAGS))

def get_raw_code(name):
    try:
        from ._shaders import name
    except ImportError:
        raise ValueError(f"'{name}' is not an available shader.")
    return name.code