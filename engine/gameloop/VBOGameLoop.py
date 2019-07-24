import pygame, numpy as np
import glm
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
        self.ambient_light = .7
        self.ambient_light_color = np.array((1.0, 1.0, 1.0))
        self.filters = filters if filters else []
        self.animators = []
        self.collision_systems = []

        self._event_handlers = {}
        self.state = {}  # a dictionary for storing in-game variables.

    def GLsetup(self, display):
        "Set up OpenGL."
        self.projection = glm.perspective(45, float(display.get_width()) / display.get_height(), .02, 5)
        # Set up the drawing field.
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glClearColor(.5, .5, .5, 0.)

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
        self.flaggo = True
        while not self.exit_flag:
            self.handle_events()
            self.animate()
            self.render()
            clock.tick(clock_rate)
        # end game loop

    def render(self):
        "Override for custom drawing."
        # Clear the screen buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for shader in self.shaders:
            with shader.rendering():
                # Set view and perspective
                glUniformMatrix4fv(
                    shader.uniforms['view'][0],
                    1,
                    GL_FALSE,
                    np.array(self.view.matrix))
                glUniformMatrix4fv(
                    shader.uniforms['projection'][0],
                    1,
                    GL_FALSE,
                    np.array(self.projection))
                glUniform1f(shader.uniforms['light_ambient_weight'][0], self.ambient_light)
                glUniform3f(shader.uniforms['light_ambient_color'][0], *self.ambient_light_color)
                glUniform3f(shader.uniforms['light_pos'][0], *(2., 2., 2.))
                glUniform3f(shader.uniforms['light_color'][0], *(1, 1, 1))
                glUniform1f(shader.uniforms['light_glare'][0], 32.)

                # Draw models with shader
                for mdl, vao in shader._models_and_VAOs:
                    # Set the model's transform matrix uniform
                    vbo, mode = mdl.render_data
                    glUniformMatrix4fv(
                        shader.uniforms['model'][0],
                        1,
                        GL_FALSE,
                        np.array(mdl.model_matrix))
                    vao.bind()
                    vbo.bind()  # Binds the VBO.
                    glDrawArrays(mode, 0, len(vbo))
                self.flaggo = False
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

    def animate(self):
        for ani in self.animators:
            ani.step()
        for coll in self.collision_systems:
            coll.detect()

    def cleanup(self):
        pass

    def create_buffers(self):
        '''
        Each model creates and stores a reference to its own
        Vertex Buffer Object (VBO).
        '''
        for shader in self.shaders:
            for model, _ in shader._models_and_VAOs:
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
