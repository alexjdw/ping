# import pygame, numpy as np
# from .Shape3D import Shape3D
# from .Point3D import Point3D
# from ..constants import WIDTH, HEIGHT
# from ..utils import vector


class Sphere3D():
    pass
#     "A sphere represented by a point and a radius."
#     def __init__(self, parent, radius, posx, posy, posz, color):
#         self.pos3d = np.array([posx, posy, posz])
#         self.vector = np.array([0., 0., 0.])
#         self.drag = 0
#         self.radius = radius
#         self.color = color
#         self.parent = parent

#     def draw(self, target):
#         scale = vector.dist(self.pos3d,
#                      np.array([self.parent.get_width(),
#                                self.parent.get_height(), 0])) ** .33
#         if not self.pos3d[2] <= 0:  # Draw nothing as the object is behind the camera.
#             pygame.draw.circle(target, self.color, self.pos, int(self.radius / scale))