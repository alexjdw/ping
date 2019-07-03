import numpy as np
from .utils import ReprMixin


class Camera(ReprMixin):
    "A camera object. Use to position viewport."
    def __init__(self):
        'Initializes the camera at 0,0,0 with no rotation.'
        self._translate = np.array((0, 0, 0), 'f')
        self._rotate = np.array((0, 0))
        self._zoom = 1

    def move(self, x, y, z):
        'Moves the camera (x, y, z) units from its current position.'
        self._translate = self._translate + (x, y, z)

    def set_position(self, x, y, z):
        'Discards the previous position and move to a new one.'
        self._translate = np.array((x, y, z))

    def rotate(self, left_angle, up_angle, zdir):
        'Rotate relatively according to the current angle.'

    def set_rotation(self, zdeg, xdeg):
        '''Discards the previous rotation and sets a new one as if the camera
        was facing forward at 0,0.'''

    def relative_zoom(self, zoom):
        '''
        Zooms in or out relative to the previous zoom.
        For instance, if the current zoom is 3x, and zoom=2,
        the new zoom will be 6x, effectively doubling the
        size of all objects in view.
        '''
        self._zoom = float(self._zoom * zoom)

    def set_zoom(self, zoom):
        'Discards the previous zoom and sets a new one.'
        self._zoom = float(zoom)

    def lookAt(self, point):
        'Rotates the camera to look at a specific point'
        # TODO
        # Translate point and camera so the camera is at 0,0,0.
        # Set rotation of camera to look at point.
        pass

    def _render_stack(self):
        yield self._rotate
        yield self._translate
        yield self._zoom
