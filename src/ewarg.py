import sdl2, math

class ewarg(object):
    def __init__(self):
        self.tiles = []
        self.tilesets = {}

    def init(self, width, height):
        self.width = width
        self.height = height
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
        for l in self.tiles:
            for tile in l:
                tile.draw(self.renderer)
        sdl2.SDL_RenderPresent(self.renderer)

    def set_tilesize(self, width, height):
        self.tile_width = width
        self.tile_height = height

        self._init_tiles()

    def load_tileset(self, name, filename):
        image = sdl2.SDL_LoadBMP(bytes(filename, 'ascii'))
        self.tilesets[name] = sdl2.SDL_CreateTextureFromSurface(self.renderer,
                                                                image)
        sdl2.SDL_FreeSurface(image)


    def set_tile(self, x, y, tileset, tile_x, tile_y):
        self.tiles[x][y].set(self.tilesets[tileset], tile_x, tile_y)

    def _init_tiles(self):
        tiles_per_row = int(math.ceil(float(self.width) / self.tile_width))
        tiles_per_col = int(math.ceil(float(self.height) / self.tile_height))
        self.tiles = []
        self.blank = sdl2.SDL_CreateTexture(self.renderer,
                                            sdl2.SDL_PIXELFORMAT_ARGB8888,
                                            sdl2.SDL_TEXTUREACCESS_STATIC,
                                            self.tile_width,
                                            self.tile_height)
        for x in range(tiles_per_row):
            self.tiles.append([])
            for y in range(tiles_per_col):
                t = Tile(x, y, self.tile_width, self.tile_height)
                t.set(self.blank, 0, 0)
                self.tiles[x].append(t)

class Tile(object):
    def __init__(self, x, y, width, height):
        self.texture = None
        self.dest = sdl2.SDL_Rect(x*width, y*height, width, height)
        self.width = width
        self.height = height

    def set(self, texture, tile_x, tile_y):
        self.texture = texture
        self.src = sdl2.SDL_Rect(tile_x*self.width, tile_y*self.height,
                                 self.width, self.height)

    def draw(self, renderer):
        sdl2.SDL_RenderCopy(renderer, self.texture, self.src, self.dest)
