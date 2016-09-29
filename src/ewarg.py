import sdl2, math, json

class ewarg(object):
    def __init__(self):
        self.tiles = []
        self.tilesets = {}
        self.sprites = {}

    def init(self, width, height):
        self.width = width
        self.height = height
        self.window = sdl2.SDL_CreateWindow(b"ewarg",
                                            sdl2.SDL_WINDOWPOS_CENTERED,
                                            sdl2.SDL_WINDOWPOS_CENTERED,
                                            width, height,
                                            sdl2.SDL_WINDOW_SHOWN)
        self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, 0)
        self.cache = TextureCache(self.renderer)

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
        self.tilesets[name] = self.cache.get(filename)

    def set_tile(self, x, y, tileset, tile_x, tile_y):
        self.tiles[x][y].set(self.tilesets[tileset], tile_x, tile_y)

    def load_sprite(self, filename):
        path = "/".join(filename.split("/")[0:-1]) + "/"
        sprite_name = filename.split("/")[-1].split(".")[0:-1][0]
        f = open(filename)
        sprite_def = json.load(f)
        f.close()
        self.sprites[sprite_name] = Sprite(sprite_def, path, self.cache)

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

class TextureCache(object):
    def __init__(self, renderer):
        self.renderer = renderer
        self.cache = {}

    def get(self, filename):
        if filename not in self.cache:
            image = sdl2.SDL_LoadBMP(bytes(filename, 'ascii'))
            self.cache[filename] = sdl2.SDL_CreateTextureFromSurface(self.renderer,
                                                                     image)
            sdl2.SDL_FreeSurface(image)
        return self.cache[filename]

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

class Sprite(object):
    def __init__(self, sprite_def, path, cache):
        self.animations = {}
        for name, animation_def in sprite_def.items():
            self.animations[name] = Animation(animation_def, path, cache)

class Animation(object):
    def __init__(self, animation_def, path, cache):
        self.frames = animation_def["frames"]
        self.texture = cache.get(path + animation_def["image"]["path"])
        self.width = animation_def["image"]["width"]
        self.height = animation_def["image"]["height"]
        self.looping = animation_def["looping"]

    def __str__(self):
        return "Width: " + str(self.width) + ", Height: " + str(self.height) + \
            ", Looping: " + str(self.looping) + ", Frames: " + str(self.frames)
