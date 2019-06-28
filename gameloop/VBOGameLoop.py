import pygame, numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

from contextlib import contextmanager


class VBOGameLoop(GameLoop):
    def __init__(self, drawables, translatefv=(0., 0., -.5), rotatefv=(0., 0., 0., 0.)):
        self.exit_flag = False
        if not isinstance(drawables, set):
            raise TypeError("drawables should be a Set. Sets provide \
                fast lookup and avoid duplicates")

        self.drawables = drawables
        self._event_handlers = {}
        self.state = {}  # a dictionary for storing in-game variables.
        self.exit_flag = False  # a flag to exit the game.
        glTranslatefv(translatefv)  # initial translation/camera angle
        glRotatefv(rotatefv)


    def Render(self, mode):
        """Render the geometry for the scene."""
        # Start applying the shader.
        

    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."

        # OpenGL setup. ################################
        # Set perspective, aspect ratio, clipping bounds
        gluPerspective(0, (display.get_width() / display.get_height()),
                       .1,
                       50.)

        # Main Loop #####################################
        self.exit_flag = False
        while not self.exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type in self._event_handlers:
                    self._event_handlers[event.type](self, event)

            # clear the screen
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            self.Render()

            pygame.display.flip()
            clock.tick(clock_rate)
        # end game loop

    def __enter__(self):  # A place to load game assets. Override as needed.
        return self

    def __exit__(self, type, value, traceback):  # Destroy game assets. Override as needed.
        "Actions performed when the class exits."
        print("Exiting game loop.")
        return False  # do not supress any errors.
