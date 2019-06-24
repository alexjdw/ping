from .drawable import Ball3D
from .vector import perpendicular_vector as perp
import numpy as np
from math import copysign


class PingPongBall(Ball3D):
    def __init__(self, *args):
        super().__init__(*args)
        # Note: The rotation effect is applied perpendicular to the direction
        # of travel of the ball and is not based on.
        
        # Spins are applied as a percentage of the original vector; stronger
        # hits = more spin. Also, topspin forces the ball down and should be
        # negative.
        self.topspin = .5
        self.sidespin = -1
        self.gravity = .6

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
        print(np.array([xz[0], yz[0], xz[1] + yz[1]]))

        self.topspin, self.sidespin = self.topspin * decay, self.sidespin * decay
        return np.array([xz[0], yz[0], xz[1] + yz[1]])