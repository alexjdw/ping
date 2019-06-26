import pygame


class GameLoop:
    def __init__(self, drawables):
        self.exit_flag = False
        if not (hasattr(drawables, '__iter__') or hasattr(drawables, '__getitem__')):
            raise TypeError("drawables must be an iterable.")
        self.drawables = drawables

    def begin(self, display, clock, clock_rate):
        "Begins the game loop on the given display."
        while not exit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

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
        raise type(value)
