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
    def __init__(self, shaders):
        self.exit_flag = False
        self.shaders = shaders
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
        # glTranslate(0,0,0)  # initial translation/camera angle
        # glRotate(0,0,0,0)   # rotate the camera
        # glScale(1,1,1)      # set the scaling
        glClearColor(.2, .2, .2, 1)

    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."
        self.exit_flag = False

        # ### Pipeline ### #
        # Compile models into VBOs
        # Prep lights, cameras
        # Load model VBOs into VBAs by shader
        # Load filters
        # ## Main Loop
        # - Handle events
        # - Draw VBAs
        # - Apply filters
        # - Show screen
        # - exit_flag = True or trigger pygame.QUIT to exit loop
        # ##
        # Event loop ends. Clean up everything.

        # Display init
        self.GLsetup(display)

        # Create buffers, compile models and put them in the buffers
        self.createBuffers()
        self.compileModels()

        # Add other objects to the scene
        self.addLighting()
        self.addCameras()

        # Main Loop
        while not self.exit_flag:
            self.handle_events()
            self.render()
            # clear the screen
            clock.tick(clock_rate)
        # end game loop

    def render(self):
        "Override for custom drawing."
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for shader in self.shaders:
            with shader.rendering():  # Apply shader program
                for m in shader.models:
                    verticies, mode, offset = d.render()
                    vbo = VBO(verticies)
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

        # TODO Apply postprocessing filters

        # Put it on the screen.
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
