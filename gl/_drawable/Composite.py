from ..utils import ReprMixin


class Composite(ReprMixin):
    def __init__(self, *drawables):
        self.drawables = drawables

    def draw(self, target):
        for d in self.drawables:
            d.draw(target)
