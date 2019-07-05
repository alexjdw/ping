import numpy as np
from .utils import ReprMixin
from .utils import transformations


class Camera(ReprMixin):
    "A camera object. Use to position viewport."
    def __init__(self):
        'Initializes the camera at 0,0,0 with no rotation.'
        self._position = np.array((0, 0, 0), 'f')
        self._rotate = np.array((0, 0))
        self._zoom = 1
        self._transm = None
        self._yaw = 0.
        self._pitch = 0.
        self._roll = 0.
        self._rotm = None
        self._zoomm = None
        self._matrix = None

    def move(self, x, y, z):
        'Moves the camera (x, y, z) units from its current position.'
        self._position = self._position + (x, y, z)
        self._transm = None

    def relative_move(self, right, up, forward):
        '''Moves the camera relative to its own current rotation.
        For instance, if the camera is facing straight down,
        relative_move()ing forward would be the same as move()ing down.'''
        # TODO
        self._matrix = None
        self._transm = None

    def set_position(self, x, y, z):
        'Discards the previous position and move to a new one.'
        self._position = np.array((x, y, z), 'f')
        self._matrix = None
        self._transm = None

    def rotate(self, left_angle, forward_angle, tilt_angle, degrees=True):
        '''
        Rotate relatively according to the current angle.

        Imagine you are looking straight ahead.
        left_angle: rotate your head to the left
        forward_angle: tilt your head back
        tilt_angle: tilt your head to the right.

        In math terms, left_angle rotates around the y axis,
        forward_angle rotates around the x axis, and tilt_angle
        rotates around the z axis.
        '''
        if degrees:
            left_angle = np.deg2rad(left_angle)
            forward_angle = np.deg2rad(forward_angle)
            tilt_angle = np.deg2rad(tilt_angle)
        self._yaw -= left_angle
        self._pitch -= forward_angle
        self._roll += tilt_angle

        self._rotm = None
        self._matrix = None

    def set_rotation(self, left_angle, forward_angle, tilt_angle, degrees=True):
        '''
        Discards the previous rotation and sets a new one as if the camera
        was facing forward (x=0, y=0, z=1) at the origin.

        :param angles:
        :param degrees: If true, input angles in degrees. If false, input
          angles in radians.
        '''
        if degrees:
            left_angle = np.degtorad(left_angle)
            forward_angle = np.degtorad(forward_angle)
            tilt_angle = np.degtorad(tilt_angle)
        self._rotm = transformations.euler_matrix(-1*tilt_angle,
                                                  -1*forward_angle,
                                                  -1*left_angle)
        self._matrix = None

    def relative_zoom(self, zoom):
        '''
        Zooms in or out relative to the previous zoom.
        For instance, if the current zoom is 3x, and zoom=2,
        the new zoom will be 6x. Zoom=2 always doubles
        the size of all objects in view.
        '''
        self._zoom = float(self._zoom * zoom)
        self._matrix = None
        self._zoomm = None

    def set_zoom(self, zoom):
        'Discards the previous zoom and sets a new one.'
        self._zoom = float(zoom)
        self._matrix = None
        self._zoomm = None

    def look_at(self, point):
        'Rotates the camera to look at a specific point'
        # TODO
        # Translate point and camera so the camera is at 0,0,0.
        # Set rotation of camera to look at point.
        pass

    @property
    def matrix(self):
        if self._matrix is None:
            if self._transm is None:
                self._transm = np.identity(4)
                self._transm[0][3], self._transm[1][3], self._transm[2][3] = self._position
            if self._zoomm is None:
                self._zoomm = np.identity(4)
                self._zoomm[0][0] = self._zoom
                self._zoomm[1][1] = self._zoom
                self._zoomm[2][2] = self._zoom
            if self._rotm is None:
                self._rotm = transformations.euler_matrix(
                                self._roll,
                                -1 * self._yaw,
                                -1 * self._pitch,
                                'szyx')

            self._matrix = np.matmul(np.matmul(self._transm, self._rotm),
                                     self._zoomm)
            print(self._matrix)

        return self._matrix
