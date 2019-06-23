import pygame
from math import sin, cos, copysign, sqrt


class Drawable:
    def __init__(self, width, height, posx, posy, image=None):
        self.surface = pygame.Surface((width, height))
        self.pos = (posx, posy)


class Mobile(Drawable):
    def __init__(self, width, height, posx, posy, image=None):
        super().__init__(width, height, posx, posy, image)
        self.vector = (0, 0)
        self.drag = 0

    def get_momentum(self):
        return sqrt(self.vector[0] ^ 2 + self.vector[1] ^ 2)

    def set_momentum(self, val):
        if self.vector[0] or self.vector[1]:
            x_scalar = abs(self.vector[0]) / (abs(self.vector[0]) + abs(self.vector[1]))
            y_scalar = 1 - x_scalar
        else:
            x_scalar = .5
            y_scalar = .5

        self.vector = (x_scalar * val, y_scalar * val)

    momentum = property(get_momentum, set_momentum)

    def move(self):
        self.pos = (self.pos[0] + self.vector[0],
                    self.pos[1] + self.vector[1])


class Point3D:
    '''A point requires a relative parent surface. The point will be
    drawn relative to the center (width / 2, height / 2) of the surface.'''
    def __init__(self, parent, x, y, z):
        self.pos3d = (x, y, z)
        self.parent = parent

    def Z(self):
        size = self.parent.get_size()
        x = self.pos3d[0] - size[0] // 2
        y = self.pos3d[1] - size[1] // 2
        z = self.pos3d[2]
        return int(sqrt(x ** 2 + y ** 2 + z ** 2))

    def draw(self):
        "Draw the point as a single pixel"
        Z = self.Z()
        pygame.gfxdraw.box(target,
                pygame.Rect(self.pos, (self.width, self.height),
                self.color))


class Shape3D(Drawable):
    '''A 3D shape that's drawn by the polygon made from a collection of points.'''
    def __init__(self, parent, width, height, points_list, color):
        self.points = points_list
        self.vector = (0, 0, 0)
        self.drag = 0
        self.width = width
        self.height = height
        self.color = color
        self.parent = parent

    def get_momentum(self):
        return sqrt(self.vector[0] ** 2 + self.vector[1] ** 2 + self.vector[2] ** 2)

    def set_momentum(self, val):
        if self.vector[0] or self.vector[1] or self.vector[2]:
            vsum = abs(self.vector[0]) + abs(self.vector[1]) + abs(self.vector[2])
            x_scalar = abs(self.vector[0]) / vsum
            y_scalar = abs(self.vector[1]) / vsum
            z_scalar = 1 - x_scalar - y_scalar
        else:
            x_scalar = .333
            y_scalar = .333
            z_scalar = .333

        self.vector = (x_scalar * val, y_scalar * val, z_scalar * val)

    momentum = property(get_momentum, set_momentum)

    @property
    def pos(self):
        Z = self.Z()
        w, h = self.parent.get_size()
        w_ratio = w / (2 * Z)
        h_ratio = h / (2 * Z)
        x = w_ratio * (self.pos3d[0] - (w / 2))
        y = h_ratio * (self.pos3d[1] - (h / 2))
        x = x + (w / 2)
        y = y + (h / 2)
        return (int(x), int(y))

    def move(self):
        self.pos3d = (self.pos3d[0] + self.vector[0],
                      self.pos3d[1] + self.vector[1],
                      self.pos3d[2] + self.vector[2])

    def draw(self, target):
        Z = self.Z()
        pygame.gfxdraw.box(target,
                pygame.Rect(self.pos, (self.width, self.height),
                self.color))


class Ball3D(Shape3D, Point3D):
    def __init__(self, parent, radius, posx, posy, posz, color):
        self.pos3d = (posx, posy, posz)
        self.vector = (0, 0, 0)
        self.drag = 0
        self.radius = radius
        self.color = color
        self.parent = parent

    def draw(self, target):
        if not self.pos3d[2] <= 0: # Draw nothing as the object is behind the camera.
            pygame.draw.circle(target, self.color, self.pos, self.radius // self.pos3d[2])


class Composite:
    def __init__(self, *args):
        self.drawables = args

    def draw(self, target):
        for d in drawables:
            d.draw(target)


class Interactable(Drawable):
    def on_click(self):
        raise NotImplementedError("Interactable forgot to override on_click")
