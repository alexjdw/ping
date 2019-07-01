import pygame, numpy as np
from OpenGL.GL import *
from OpenGL.GL import glTranslate, glRotate, glLoadIdentity,\
    glClearColor, glClear, glDisableClientState, glEnableClientState,\
    glVertexPointerf, glDrawArrays, glGetError, shaders,\
    glScale,\
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_VERTEX_ARRAY
from OpenGL.GLU import *
from OpenGL.GLU import gluPerspective
from OpenGL.arrays.vbo import VBO
from .GameLoop import GameLoop
from contextlib import contextmanager


class VBOGameLoop(GameLoop):
    def __init__(self, drawables, translate=(0., 0., -.1), rotate=(0., 0., 0., 0.)):
        self.exit_flag = False
        if not isinstance(drawables, set):
            raise TypeError("drawables should be a Set. Sets provide \
                fast lookup and avoid duplicates")

        self.drawables = drawables
        self._event_handlers = {}
        self.state = {}  # a dictionary for storing in-game variables.
        self.exit_flag = False  # a flag to exit the game.
        self.translate = translate
        self.rotate = rotate

    def GLsetup(self, display):
        "Set up OpenGL."
        glLoadIdentity()

        # Set up the drawing field.
        # https://www.sjbaker.org/steve/omniv/projection_abuse.html
        glMatrixMode(GL_PROJECTION)
        gluPerspective(0, 
                       (display.get_width() / display.get_height()),
                       .1,
                       10.)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        # Drawing mode.
        glMatrixMode(GL_MODELVIEW)
        glTranslate(*self.translate)  # initial translation/camera angle
        glRotate(*self.rotate)
        glClearColor(.2,.2,.2,1)

    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."
        self.GLsetup(display)
        self.exit_flag = False

        # Main Loop
        while not self.exit_flag:
            self.handle_events()
            self.render()
            # clear the screen
            clock.tick(clock_rate)
        # end game loop

    def render(self):
        "Override for custom drawing."
        # Render all the things
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for d in self.drawables:
            verticies, shader, mode = d.render()
            vbo = VBO(verticies)
            try:
                # Add the shader.
                shaders.glUseProgram(shader)
                try:
                    # Add the VBO to gfxcard memory
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

    def handle_events(self):
        "Override for custom event handling."
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type in self._event_handlers:
                self._event_handlers[event.type](self, event)


    def __enter__(self):  # A place to load game assets. Override as needed.
        return self

    def __exit__(self, type, value, traceback):  # Destroy game assets. Override as needed.
        "Actions performed when the class exits."
        return False  # do not supress any errors.
