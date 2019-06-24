import pygame
import numpy as np
from math import sin, cos, copysign, sqrt


class Drawable:
    def __init__(self, width, height, posx, posy, image=None):
        self.surface = pygame.Surface((width, height))
        self.pos = np.array([posx, posy])


class Mobile(Drawable):
    def __init__(self, width, height, posx, posy, image=None):
        super().__init__(width, height, posx, posy, image)
        self.vector = np.array([0, 0])
        self.drag = 0

    def move(self):
        self.pos = np.array([self.pos[0] + self.vector[0],
                    self.pos[1] + self.vector[1]])


class Point3D:
    '''A point requires a relative parent surface. The point will be
    drawn relative to the center (width / 2, height / 2) of the surface.'''
    def __init__(self, parent, x, y, z):
        self.pos3d = np.array([x, y, z])
        self.parent = parent

    # def Z(self):
    #     size = self.parent.get_size()
    #     x = self.pos3d[0] - size[0] / 2
    #     y = self.pos3d[1] - size[1] / 2
    #     z = self.pos3d[2]
    #     return sqrt(x ** 2 + y ** 2 + z ** 2)

    @property
    def pos(self):
        # print("Pos3d on pos: ", self.pos3d)
        # Z = self.Z()
        # w, h = self.parent.get_size()

        # # midpoints
        # w = w / 2
        # h = h / 2

        # # ratio of Z to midpoints
        # w_ratio = w / Z
        # h_ratio = h / Z

        # # Scale the distance from the midpoints, then add the midpoints back
        # x = w_ratio * (self.pos3d[0] - w) + w
        # y = h_ratio * (self.pos3d[1] - h) + h

        # print("Diff: ", self.pos3d[1] - y, '\n', np.array([int(x), int(y)]))
        # return np.array([int(x), int(y)])
        scale = self.pos3d[2] ** .33
        return (int(self.pos3d[0] * scale), int(self.pos3d[1] * scale))

    def move(self):
        self.pos3d = self.pos3d + self.vector

    def draw(self):
        "Draw the point as a single pixel"
        Z = self.Z()
        pygame.gfxdraw.box(target,
                pygame.Rect(self.pos, (self.width, self.height),
                self.color))


class Shape3D(Drawable):
    '''A 3D shape that's drawn by the polygon made from a collection of points.'''
    def __init__(self, points_list, color):
        self.points = points_list
        self.vector = np.array([0., 0., 0.])
        self.color = color

    def get_momentum(self):
        return sqrt(self.vector[0] ** 2 + self.vector[1] ** 2 + self.vector[2] ** 2)

    def set_momentum(self, val):
        vsum = abs(self.vector[0]) + abs(self.vector[1]) + abs(self.vector[2])
        if (vsum):
            scalar = val / vsum
            self.vector = self.vector * [scalar]

        else:
            self.vector = np.array([0., 0., 0.])

    momentum = property(get_momentum, set_momentum)

    def draw(self, target):
        points = [p.pos for p in self.points]
        pygame.draw.polygon(target, self.color, points)


class Ball3D(Shape3D, Point3D):
    def __init__(self, parent, radius, posx, posy, posz, color):
        self.pos3d = np.array([posx, posy, posz])
        self.vector = np.array([0., 0., 0.])
        self.drag = 0
        self.radius = radius
        self.color = color
        self.parent = parent

    def draw(self, target):
        if not self.pos3d[2] <= 0:  # Draw nothing as the object is behind the camera.
            pygame.draw.circle(target, self.color, self.pos, int(self.radius / self.pos3d[2]))


class Composite:
    def __init__(self, *args):
        self.drawables = args

    def draw(self, target):
        for d in drawables:
            d.draw(target)


class Interactable(Drawable):
    def on_click(self):
        raise NotImplementedError("Interactable forgot to override on_click")
