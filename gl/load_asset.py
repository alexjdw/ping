from .drawable import Shape3D

def load2d():
    "Loads a sprite into memory."
    pass

class Model(Shape3D):
    "A collections of vertecies, data, and textures that make up a 3D model."

    def from_obj_file(self):
        "Constructor for .obj file format. Not all features are supported."

# TODO: Asset group context manager.