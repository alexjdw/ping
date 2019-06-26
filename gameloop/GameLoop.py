import pygame


class GameLoop:
    def __init__(self, drawables):
        self.exit_flag = False
        if not (hasattr(drawables, '__iter__') or hasattr(drawables, '__getitem__')):
            raise TypeError("drawables must be an iterable.")
        self.drawables = drawables
        self._event_handlers = {}
        self.state = {}  # a dictionary for storing in-game variables.

    def define_handler(self, pygame_event, handler):
        '''
        A nice semantic way to add event handler functions to the game.
        An example of MOUSEBUTTONDOWN handler.
        def handle_click(loop, event):
            # loop: the event loop will pass itself in.
            # event: the event object from pygame
            if button == 1:  # left click
                loop.state['MOUSEDOWN'] = true  # set the loop state 
                loop.drawables.append(potato)   # show a potato

        Common pygame events and their params:
            ACTIVEEVENT      gain, state
            KEYDOWN          unicode, key, mod
            KEYUP            key, mod
            MOUSEMOTION      pos, rel, buttons
            MOUSEBUTTONUP    pos, button
            MOUSEBUTTONDOWN  pos, button
            JOYAXISMOTION    joy, axis, value
            JOYBALLMOTION    joy, ball, rel
            JOYHATMOTION     joy, hat, value
            JOYBUTTONUP      joy, button
            JOYBUTTONDOWN    joy, button
            VIDEORESIZE      size, w, h
            VIDEOEXPOSE      none
            USEREVENT        code

            
        Note: pygame.QUIT is not overridable to avoid jerks.
        '''
        self._event_handlers[pygame_event] = handler

    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."
        self.exit_flag = False
        while not self.exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type in self._event_handlers:
                    self._event_handlers[event.type](self, event)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) # clear the screen
            for d in drawables:
                if (hasattr(d, 'GLDraw')):
                    d.GLDraw()
                elif (hasattr(d, 'surface')):
                    display.blit(d.surface, d.pos)
                else:
                    raise TypeError("Drawable " + repr(d) + " can't be drawn. Please add a .survace or .draw() method.")
                if (hasattr(d, 'move')):
                    d.move()

        pygame.display.flip()
        clock.tick(clock_rate)

    def __enter__(self):  # A good place to load game assets. Override as needed.
        "Actions performed when the class is created using a 'with' statement."
        pass

    def __exit__(self, type, value, traceback):  # Destroy game assets. Override as needed.
        "Actions performed when the loop exits."
        if (type):
            raise type(value)  # Reraise the error.
