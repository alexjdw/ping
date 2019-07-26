import glm


def bounce(self, other):
    for t in self.handler_targets:
        t.momentum = t.momentum * other.bounce_rebound * other.bounce_normal
