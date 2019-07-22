from .physicsanimator import PhysicsAnimator


class GravityAnimator(PhysicsAnimator):
    def __init__(self, force, *args, **kwargs):
        ':param force: amount of velocity to add per step.'
        super().__init__(self, *args, **kwargs)
        self.translatestack = [glm.vec3(0., -1 * force, 0.)]

    def step(self):
        steps = len(self.translatestack) - 2
        if steps > 0:
            for i in range(steps):
                self.translatestack[i + 1] += self.translatestack[i]

        for model in self.targets:
            model.move(self.translatestack[-1])
