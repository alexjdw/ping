from ..utils import ReprMixin

class Animator(ReprMixin):
    'Base class template for animations.'
    def __init__(self):
        self.models = []

    def step(self):
        pass

    def apply_to(self, target):
        self.models.append(target)