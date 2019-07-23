from ..Animator import Animator
import glm

def BounceAnimator(Animator):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_collision(self):
        self.momentum.y = self.momentum.y * -1
        self.momentum = self.momentum * .95
