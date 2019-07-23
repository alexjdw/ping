def bounce(self, other):
    self.momentum = self.momentum * glm.vec3(.95, -.95, .95)