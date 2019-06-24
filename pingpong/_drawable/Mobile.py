import numpy as np
from .Drawable import Drawable


class Mobile(Drawable):
    def __init__(self, width, height, posx, posy, image=None):
        super().__init__(width, height, posx, posy, image)
        self.vector = np.array([0, 0])
        self.drag = 0

    def move(self):
        self.pos = np.array([self.pos[0] + self.vector[0],
                    self.pos[1] + self.vector[1]])