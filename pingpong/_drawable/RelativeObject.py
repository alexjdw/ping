import numpy as np

class RelativePoint:
    '''Creates a new point by injecting an offset when pos3d is accessed.'''
    def __init__(self, rel_obj, anchor_point, offset):
        if not hasattr(rel_obj, 'pos3d'):
            raise TypeError('''Invalid argument: rel_obj doesn't have a pos3d
                    attribute. This usually means you passed in the wrong
                    object type. It should be a Point3D or similar.''')

        _pos3d = np.array(rel_obj.pos3d)

        # Becometh the rel_obj. Add some obfuscated properties to avoid collision.
        self.__dict__ = {**self.__dict__, **rel_obj.__dict__}
        self._rel__offset = offset
        self._rel__anchor = anchor_point

    def _get_pos3d(self):
        return sum(self._rel__anchor) + self._rel__offset

    def _set_pos3d(self, pos3d):
        self._rel__offset = np.array(pos3d)

    pos3d = property(_get_pos3d, _set_pos3d)
