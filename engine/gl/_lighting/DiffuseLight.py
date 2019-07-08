from ..utils import ReprMixin


class DiffuseLight(ReprMixin):
    "A diffuse light that simulates a nearby glowing light source, such as a light bulb."
    def __init__(self, position, dir_vector, intensity):
        self.set_position(*position)

    def set_direction(dir_vector):
        self.direction 

    def set_position(x, y, z):
        self._pos = np.array(x, y, z)

    def look_at(point):
        # TODO
        pass
