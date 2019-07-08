import pygame, numpy as np
from OpenGL.GL import *
from OpenGL.GL import glTranslate, glRotate, glLoadIdentity,\
    glClearColor, glClear, glDisableClientState, glEnableClientState,\
    glVertexPointerf, glDrawArrays, glGetError, shaders,\
    glScale, glEnable, glHint,\
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_VERTEX_ARRAY
from OpenGL.GLU import *
from OpenGL.GLU import gluPerspective
from OpenGL.arrays.vbo import VBO
from .GameLoop import GameLoop
from contextlib import contextmanager


class VBOGameLoop(GameLoop):
    "A game loop that draws with Vertex Buffer Objects."
    def __init__(self, shaders=None, cameras=None, lights=None, filters=None):
        self.shaders = shaders if shaders else []
        self.cameras = cameras if cameras else []
        self.view = cameras[0] if len(cameras) else None
        self.lights = lights if lights else []
        self.ambient_light = 0
        self.filters = filters if filters else []

        self._event_handlers = {}
        self.state = {}  # a dictionary for storing in-game variables.

    def GLsetup(self, display):
        "Set up OpenGL."
        near = .1
        far = 100.
        fov = np.deg2rad(45)
        aspect = display.get_width() / display.get_height()
        r = np.tan(fov/2) * near
        Sx = (2 * near)/(r * aspect + r * aspect)
        Sy = near/r
        Sz = -1 * (far + near)/(far - near)
        Pz = -1 * (2 * far * near)/(far - near)
        self.perspective = np.array(
            [[Sx, 0, 0, 0],
             [0, Sy, 0, 0],
             [0, 0, Sz, Pz],
             [0, 0, -1, 0]]
        )

        # Set up the drawing field.
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        # Drawing mode.


    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."
        self.exit_flag = False

        # ### Pipeline ### #
        # Initialize the display
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
        self.create_buffers()

        # Add other objects to the scene
        self.add_lighting()
        self.add_cameras()

        # Main Loop
        while not self.exit_flag:
            self.handle_events()
            self.render()
            clock.tick(clock_rate)
        # end game loop

    def render(self):
        "Override for custom drawing."
        # Clear the screen buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for shader in self.shaders:
            with shader.rendering():
                # Draw models with shader
                for m in shader._models:
                    vbo, mode = m.render_data
                    try:
                        vbo.bind()
                        glDrawArrays(mode, 0, len(vbo))
                    finally:
                        vbo.unbind()
        glLoadIdentity()
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

    def cleanup(self):
        pass

    def create_buffers(self):
        '''
        Each model creates and stores a reference to its own
        Vertex Buffer Object (VBO).
        '''
        for shader in self.shaders:
            for model in shader._models:
                model.compile_VBO()

    def add_lighting(self):
        pass

    def add_cameras(self):
        pass

    def __enter__(self):  # A place to load game assets. Override as needed.
        return self

    def __exit__(self, type, value, traceback):  # Destroy game assets. Override as needed.
        "Actions performed when the class exits."
        return False  # do not supress any errors.
