from .GameLoop import GameLoop
from sys import path


class PingPongMatch(VBOGameLoop):
    def __enter__(self):
        # Load the following assets.
        with open(path.join('..', 'assets', 'pingpong.assets')) as assets:
            self.VBOs = {}
