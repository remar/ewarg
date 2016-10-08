import sdl2, math, json, sdl2.sdlgfx

class ewarg(object):
    def __init__(self):
        self.tiles = []
        self.tilesets = {}
        self.sprites = {}
        self.sprite_instances = {}
        self.next_sprite_id = 0
        self.last_time = 0
        self.fps_manager = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_initFramerate(self.fps_manager)
        sdl2.sdlgfx.SDL_setFramerate(self.fps_manager, 60)

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
        if self.last_time == 0:
            delta = 0
        else:
            delta = sdl2.SDL_GetTicks() - self.last_time
        self.last_time = sdl2.SDL_GetTicks()

        sdl2.SDL_RenderClear(self.renderer)

        for l in self.tiles:
            for tile in l:
                tile.draw(self.renderer)

        for sprite_instance in self.sprite_instances.values():
            sprite_instance.draw(self.renderer, delta)

        sdl2.SDL_RenderPresent(self.renderer)

        sdl2.sdlgfx.SDL_framerateDelay(self.fps_manager)

    def set_tilesize(self, width, height):
        self.tile_width = width
        self.tile_height = height

        self._init_tiles()

    def load_tileset(self, name, filename):
        self.tilesets[name] = self.cache.get(filename)

    def set_tile(self, x, y, tileset, tile_x, tile_y):
        self.tiles[x][y].set(self.tilesets[tileset], tile_x, tile_y)

    def load_sprite(self, filename):
        path = "/".join(filename.split("/")[0:-1])
        if path != "":
            path = path + "/"
        sprite_name = filename.split("/")[-1].split(".")[0:-1][0]
        f = open(filename)
        sprite_def = json.load(f)
        f.close()
        self.sprites[sprite_name] = Sprite(sprite_def, path, self.cache)

    def create_sprite_instance(self, sprite_name):
        sprite_id = self.next_sprite_id
        self.next_sprite_id += 1
        self.sprite_instances[sprite_id] = SpriteInstance(self.sprites[sprite_name])
        return sprite_id

    def remove_sprite_instance(self, sprite_id):
        del self.sprite_instances[sprite_id]

    def show_sprite(self, sprite_id, show):
        self.sprite_instances[sprite_id].set_visible(show)

    def set_animation(self, sprite_id, animation):
        self.sprite_instances[sprite_id].set_animation(animation)

    def move_sprite_rel(self, sprite_id, dx, dy):
        self.sprite_instances[sprite_id].move_rel(dx, dy)

    def move_sprite_abs(self, sprite_id, x, y):
        self.sprite_instances[sprite_id].move_abs(x, y)

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

    def __str__(self):
        return "\n".join(map(str, self.animations.values()))

class Animation(object):
    def __init__(self, animation_def, path, cache):
        self.frames = animation_def["frames"]
        self.texture = cache.get(path + animation_def["image"]["path"])
        self.width = animation_def["image"]["width"]
        self.height = animation_def["image"]["height"]
        self.looping = animation_def["looping"]

    def __str__(self):
        return "Frames: " + str(self.frames) + ", width: " + str(self.width) \
            + ", height: " + str(self.height) + ", looping: " \
            + str(self.looping)

class SpriteInstance(object):
    def __init__(self, sprite):
        self.sprite = sprite
        self.current_animation = None
        self.visible = True
        self.current_frame = 0
        self.time_spent_in_frame = 0
        self.src = sdl2.SDL_Rect()
        self.dest = sdl2.SDL_Rect()

    def set_animation(self, animation):
        self.current_animation = self.sprite.animations[animation]
        self.frames_len = len(self.current_animation.frames)
        self.current_frame_index = 0
        self.current_frame = self.current_animation.frames[self.current_frame_index]
        self.current_frame_time = self.current_frame[1]
        self.time_spent_in_frame = 0
        self.texture = self.current_animation.texture

        self.dest.w = self.src.w = self.current_animation.width
        self.dest.h = self.src.h = self.current_animation.height

        self.src.x = self.current_frame[0] * self.current_animation.width

    def set_visible(self, visible):
        self.visible = visible

    def draw(self, renderer, delta):
        self._animate(delta)
        if self.current_animation != None and self.visible and self.current_frame[0] != -1:
            sdl2.SDL_RenderCopy(renderer, self.texture, self.src, self.dest)

    def move_rel(self, dx, dy):
        self.dest.x += dx
        self.dest.y += dy

    def move_abs(self, x, y):
        self.dest.x = x
        self.dest.y = y

    def _animate(self, delta):
        self.time_spent_in_frame += delta
        if self.time_spent_in_frame > self.current_frame_time:
            self._next_frame()
            # go to next frame

    def _next_frame(self):
        if self.current_frame_index + 1 == self.frames_len:
            if self.current_animation.looping:
                self.current_frame_index = 0
            else:
                return # We're at the last frame and we're not looping
        else:
            self.current_frame_index += 1

        self.current_frame = self.current_animation.frames[self.current_frame_index]
        self.current_frame_time = self.current_frame[1]
        self.time_spent_in_frame = 0

        self.src.x = self.current_frame[0] * self.current_animation.width
