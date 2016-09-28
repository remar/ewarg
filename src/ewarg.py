import sdl2

class ewarg(object):
    def __init__(self):
        # TODO: set up data structures for tilesets, sprites, and sprite
        # instances
        pass

    def init(self, width, height):
        self.window = sdl2.SDL_CreateWindow(b"ewarg",
                                            sdl2.SDL_WINDOWPOS_CENTERED,
                                            sdl2.SDL_WINDOWPOS_CENTERED,
                                            width, height,
                                            sdl2.SDL_WINDOW_SHOWN)
        self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, 0)

        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"linear")
        sdl2.SDL_RenderSetLogicalSize(self.renderer, width, height)

    def redraw(self):
        sdl2.SDL_RenderClear(self.renderer)
        sdl2.SDL_RenderPresent(self.renderer)

    def set_background_color(self, r, g, b):
        sdl2.SDL_SetRenderDrawColor(self.renderer, r, g, b, 255)
