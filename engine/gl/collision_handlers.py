import glm


def bounce(self, other):
    for t in self.handler_targets:
        print(">", t.momentum)
        t.momentum = t.momentum * glm.vec3(.95, -.95, .95)
        print(">>", t.momentum)
