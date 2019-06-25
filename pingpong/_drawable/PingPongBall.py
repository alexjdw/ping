from .Ball3D import Ball3D
from ..utils import vector
import numpy as np

perp = vector.perpendicular_vector


class PingPongBall(Ball3D):
    def __init__(self, *args):
        super().__init__(*args)
        # Note: The rotation effect is applied perpendicular to the direction
        # of travel of the ball and is not based on.

        # Spins are applied as a percentage of the original vector; stronger
        # hits = more spin. Also, topspin forces the ball down and should be
        # negative.
        self.topspin = 0
        self.sidespin = 0
        self.gravity = 0

        self.debug = 0

    def move(self):
        super().move()

        drag = .99
        # Apply gravity
        self.vector[1] = self.vector[1] + self.gravity
        v = self.vector
        self.vector = self.vector + self.rot_vector

    @property
    def rot_vector(self):
        decay = .05

        # perp of vectors
        xz = np.array([-1 * self.vector[2], self.vector[0]]) * self.sidespin
        yz = np.array([-1 * self.vector[2], self.vector[1]]) * self.topspin

        self.topspin, self.sidespin = self.topspin * decay, self.sidespin * decay
        return np.array([xz[0], yz[0], xz[1] + yz[1]])

    def check_collision(self, obj):
        pass
