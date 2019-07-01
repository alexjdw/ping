from .Shape3D import Shape3D
from contextlib import contextmanager
from ..obj_loader import OBJ

class Model3D(Shape3D):
    pass

def load(file):
    ":param file: The absolute path of the file, joined by os_path_join"
    ext = file.split('.')[-1]  # file extension
    if ext is "obj":
        return OBJ(file)