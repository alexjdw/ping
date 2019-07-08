from .DiffuseLight import DiffuseLight


class SkyLight(DiffuseLight):
    def __init__(self, direction):
        self.set_direction(direction)

    "A diffuse light that simulates a far-away light, such as the sun or moon."
    def set_direction(self, dir_vector):
        self.direction = dir_vector
