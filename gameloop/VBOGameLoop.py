import pygame, numpy as np
from OpenGL.GL import glTranslate, glRotate, gluPerspective, glLoadIdentity,\
    glClearColor, glClear, glDisableClientState, glEnableClientState,\
    glVertexPointerf, glDrawArrays, glGetError, shaders
from OpenGL.GLU import *
from OpenGL.arrays.vbo import VBO
from .GameLoop import GameLoop
from contextlib import contextmanager

class VBOGameLoop(GameLoop):
    def __init__(self, drawables, translatev=(0., 0., -1), rotatev=(0., 0., 0., 0.)):
        self.exit_flag = False
        if not isinstance(drawables, set):
            raise TypeError("drawables should be a Set. Sets provide \
                fast lookup and avoid duplicates")

        self.drawables = drawables
        self._event_handlers = {}
        self.state = {}  # a dictionary for storing in-game variables.
        self.exit_flag = False  # a flag to exit the game.
        glTranslate(*translatev)  # initial translation/camera angle
        glRotate(*rotatev)


    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."

        # OpenGL setup. ################################
        # Set perspective, aspect ratio, clipping bound.
        gluPerspective(0, (display.get_width() / display.get_height()),
                       .1,
                       1.)
        glLoadIdentity()

        glClearColor(.2,.2,.2,1) 
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

            # Render all the things
            for d in self.drawables:
                verticies, shader, mode = d.to_renderable()
                vbo = VBO(verticies)
                try:
                    # Add the VBO to gfxcard memory
                    shaders.glUseProgram(shader)
                    assert not glGetError()
                    try:
                        vbo.bind()
                        glEnableClientState(GL_VERTEX_ARRAY)
                        glVertexPointerf(vbo)
                        glDrawArrays(mode, 0, len(verticies))
                    finally:
                        # Release the VBO memory in the graphics card
                        vbo.unbind()
                        glDisableClientState(GL_VERTEX_ARRAY)
                finally:
                    # Remove the shader
                    shaders.glUseProgram(0)


            pygame.display.flip()
            clock.tick(clock_rate)
        # end game loop

    def __enter__(self):  # A place to load game assets. Override as needed.
        return self

    def __exit__(self, type, value, traceback):  # Destroy game assets. Override as needed.
        "Actions performed when the class exits."
        print("Exiting game loop.")
        return False  # do not supress any errors.
