from .Drawable import Drawable


class Interactable(Drawable):
    def on_click(self):
        raise NotImplementedError("Interactable forgot to override on_click")
