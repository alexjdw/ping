import pygame


class Menu:
    def __init__(self, bg, interactables):
        self.bg = pygame.image.load(bg)
        self.interactables = interactables

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        for i in self.interactables:
            surface.blit(i.draw(), i.pos)
