from .Shape3D import Shape3D
from .Point3D import Point3D


class Ball3D(Shape3D, Point3D):
    "A sphere represented by a point and a radius."
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
