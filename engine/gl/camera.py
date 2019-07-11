import numpy as np
from .utils import ReprMixin
from .utils import transformations
import glm

class Camera(ReprMixin):
    "A camera object. Use to position the viewport."
    def __init__(self):
        'Initializes the camera at 0,0,0 with no rotation.'
        self._position = glm.vec3(0, 0, 0)
        self._zoom = 1
        self._transm = None
        self._yaw = 0.
        self._pitch = 0.
        self._roll = 0.
        self._rotm = None
        self._zoomm = None
        self._matrix = None
        self._fov = None

    def move(self, x, y, z):
        'Moves the camera (x, y, z) units from its current position in world space.'
        self._position = self._position + (x, y, z)
        self._transm = None

    def relative_move(self, right, up, forward):
        '''Moves the camera relative to its own current rotation.
        For instance, if the camera is facing straight down,
        relative_move()ing forward would be the same as move()ing down.'''
        cyaw = glm.cos(self._yaw)
        syaw = glm.sin(self._yaw)
        cpitch = glm.cos(self._pitch)
        spitch = glm.sin(self._pitch)
        croll = glm.cos(self._roll)
        sroll = glm.sin(self._roll)
        x = (-1 * cyaw * syaw * sroll - sroll * croll) * right
        y = (-1 * syaw * spitch * sroll + cyaw * croll) * up
        z = -1 * (cpitch * sroll) * forward
        self._position = self._position + glm.vec3(x, y, z)
        self._transm = None
        self._matrix = None

    def set_position(self, x, y, z):
        'Discards the previous position and move to a new one.'
        self._position = glm.vec4(x, y, z)
        self._transm = None
        self._matrix = None

    def rotate(self, yaw, pitch, roll, degrees=True):
        '''
        Rotate relatively according to the current angle.

        In math terms, left_angle rotates around the y axis,
        forward_angle rotates around the x axis, and tilt_angle
        rotates around the z axis.
        '''
        if degrees:
            yaw = np.deg2rad(yaw)
            pitch = np.deg2rad(pitch)
            roll = np.deg2rad(roll)
        self._yaw -= yaw
        self._pitch -= pitch
        self._roll += roll

        self._rotm = None
        self._matrix = None

    def set_rotation(self, yaw, pitch, roll, degrees=True):
        '''
        Discards the previous rotation and sets a new one as if the camera
        was facing forward (x=0, y=0, z=1) at the origin.

        :param degrees: If true, input angles in degrees. If false, input
          angles in radians.
        '''
        if degrees:
            yaw = np.deg2rad(yaw)
            pitch = np.deg2rad(pitch)
            roll = np.deg2rad(roll)
        self._yaw = yaw
        self._pitch = pitch
        self._roll = roll
        self._rotm = None
        self._matrix = None

    def zoom(self, zoom):
        '''
        Zooms in or out relative to the previous zoom.
        For instance, if the current zoom is 3x, and zoom=2,
        the new zoom will be 6x.
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
        'Rotates the camera to look at a specific point.'
        p = point - self._position
        up = (-1 * glm.sin(self._yaw) * glm.sin(self._pitch)
              * glm.sin(self._roll) + glm.cos(self._yaw)
              * glm.cos(self._roll))
        self._rotm = glm.lookAt(glm.vec3(0, 0, 0), p, up)

    @property
    def matrix(self):
        if self._matrix is None:
            if self._transm is None:
                self._transm = glm.translate(glm.mat4(), self._position)
                print(self._transm)
            if self._zoomm is None:
                self._zoomm = glm.mat4()
                self._zoomm[0][0] = self._zoom
                self._zoomm[1][1] = self._zoom
                self._zoomm[2][2] = self._zoom
            if self._rotm is None:
                self._rotm = transformations.euler_matrix(
                                -1 * self._roll,
                                -1 * self._yaw,
                                -1 * self._pitch,
                                'szyx')
            self._matrix = self._transm * self._zoomm * self._rotm

        return self._matrix
