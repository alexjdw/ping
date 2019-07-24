from ..Animator import Animator
import glm


class PhysicsAnimator(Animator):
    "General-purpose animator for adding motion forces to an object."
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.rotatestack = [glm.vec3(0., 0., 0.)]
        self.translatestack = [glm.vec3(0., 0., 0.)]

    def step(self):
        steps = len(self.rotatestack) - 2
        if steps > 0:
            for i in range(steps):
                self.rotatestack[i + 1] += self.rotatestack[i]
        steps = len(self.translatestack) - 2
        if steps > 0:
            for i in range(steps):
                self.translatestack[i + 1] += self.translatestack[i]

        for model in self.targets:
            model.rotate(self.rotatestack[-1])
            model.move(self.translatestack[-1])

    def get_momentum(self):
        return self.translatestack[-1]

    def set_momentum(self, val):
        self.translatestack[-1] = val

    momentum = property(get_momentum, set_momentum)