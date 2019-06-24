from ..utils import ReprMixin


class Drawable(ReprMixin):
    def __init__(self, width, height, posx, posy, image=None):
        self.surface = pygame.Surface((width, height))
        self.pos = np.array([posx, posy])