from ..utils import ReprMixin

class Animator(ReprMixin):
    'Base class template for animations.'
    def __init__(self, *args, **kwargs):
        self.targets = []

    def step(self):
        pass

    def apply_to(self, target):
        self.targets.append(target)