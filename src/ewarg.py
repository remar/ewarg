# ewarg -- Python graphics engine

import pygame, math, json

class ewarg(object):
    def __init__(self):
        self.version = (0, 1, 0)
        self.tiles = []
        self.tilesets = {}
        self.sprites = {}
        self.sprite_instances = {}
        self.next_sprite_id = 0
        self.last_time = 0
        self.clock = pygame.time.Clock()
        self.frame_rate = 60

    def init(self, width, height):
        """Initializes ewarg and sets up a window."""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("ewarg")
        self.cache = TextureCache()

    def get_version(self):
        """Returns the version of this ewarg."""
        return self.version

    def redraw(self):
        """Redraw the screen with any tile changes and sprite updates.

        Call this once each frame. This function will limit the
        framerate to 60 frames per second."""
        if self.last_time == 0:
            delta = 0
        else:
            delta = pygame.time.get_ticks() - self.last_time
        self.last_time = pygame.time.get_ticks()

        self.screen.fill((0, 0, 0)) # Fill with black

        for l in self.tiles:
            for tile in l:
                tile.draw(self.screen)

        for sprite_instance in self.sprite_instances.values():
            sprite_instance.draw(self.screen, delta)

        pygame.display.flip()

        self.clock.tick(self.frame_rate)

    def set_tilesize(self, width, height):
        """Set up how big each tile should be in the background."""
        self.tile_width = width
        self.tile_height = height

        self._init_tiles()

    def load_tileset(self, name, filename):
        """Load a tileset and associate it with the given name.

        The image must be in Windows BMP format.
        """
        self.tilesets[name] = self.cache.get(filename)

    def set_tile(self, x, y, tileset, tile_x, tile_y):
        """Set a tile in the background.

        Keyword arguments:
        x -- x position of tile in the background
        y -- t position of tile in the background
        tileset -- name of previously loaded tileset
        tile_x -- x position of tile in tileset
        tile_y -- y position of tile in tileset
        """
        self.tiles[x][y].set(self.tilesets[tileset], tile_x, tile_y)

    def load_sprite(self, filename):
        """Loads a sprite specified in a JSON file.

        The loaded sprite will get the same name as the JSON file, so
        e.g. a file named mario.json will make a "mario" sprite
        available in ewarg.

        The JSON file contains a number of animation definitions. Each
        animation definition in turn contains an image definition, a
        looping attribute, and a list of frames. So a prototypical
        sprite definition looks like this:

        {
          "animation 1" : {
            "image": {
              "path": "path/to/image.bmp",
              "width": 32,
              "height": 32
            },
            "looping": true,
            "frames": [
              [0, 100], [1, 150], [2, 100]
            ]
          }
        }

        The above sprite definition will make available a sprite with
        one animation, called "animation 1".

        The image of the animation is "path/to/image.bmp", and this
        path is relative to the JSON file. The width and height
        attributes specify how big each frame of the animation is. The
        frames in the image should be laid out horizontally (in a
        row), so frame 0 is the first image, frame 1 is the second and
        so on.

        The looping attribute specifies if the animation should begin
        at the first frame after finishing the last.

        The frames array contains the frame definitions. Each frame is
        specified as an array with two elements. The first element is
        the index into the image. The second is the number of
        milliseconds this frame should be displayed. So e.g. a frame
        definition of [0, 100] means the first image, displayed 100
        milliseconds.

        A special value of -1 as image index indicates that the sprite
        should be hidden during the frames duration. So to hide a
        sprite for 150 ms, a frame definition of [-1, 150] would do
        the trick.

        See the examples that comes with ewarg for a better grasp of
        how sprite definitions work.

        """
        path = "/".join(filename.split("/")[0:-1])
        if path != "":
            path = path + "/"
        sprite_name = filename.split("/")[-1].split(".")[0:-1][0]
        f = open(filename)
        sprite_def = json.load(f)
        f.close()
        self.sprites[sprite_name] = Sprite(sprite_def, path, self.cache)

    def create_sprite_instance(self, sprite_name):
        """Creates a sprite from the given sprite definition.

        To make a sprite appear on the screen it needs to be
        instantiated. You can make any number of instances of a sprite
        definition. The return value is a sprite ID that should be used
        with other sprite methods when modifying this sprite instance.

        The created sprite instance will be visible, it will be
        located at x = 0 and y = 0, and some animation will be
        chosen. To modify this behaviour, use the other provided
        sprite methods.

        """
        sprite_id = self.next_sprite_id
        self.next_sprite_id += 1
        self.sprite_instances[sprite_id] = SpriteInstance(self.sprites[sprite_name])
        return sprite_id

    def remove_sprite_instance(self, sprite_id):
        """Remove the indicated sprite instance."""
        del self.sprite_instances[sprite_id]

    def show_sprite(self, sprite_id, show):
        """Set this sprite instance visible or invisible."""
        self.sprite_instances[sprite_id].set_visible(show)

    def set_animation(self, sprite_id, animation):
        """Set the sprite instances animation."""
        self.sprite_instances[sprite_id].set_animation(animation)

    def move_sprite_rel(self, sprite_id, dx, dy):
        """Move the sprite instance relative to its current position."""
        self.sprite_instances[sprite_id].move_rel(dx, dy)

    def move_sprite_abs(self, sprite_id, x, y):
        """Move the sprite instance to the given coordinates."""
        self.sprite_instances[sprite_id].move_abs(x, y)

    def _init_tiles(self):
        tiles_per_row = int(math.ceil(float(self.width) / self.tile_width))
        tiles_per_col = int(math.ceil(float(self.height) / self.tile_height))
        self.tiles = []
        self.blank = pygame.Surface((self.tile_width, self.tile_height))
        for x in range(tiles_per_row):
            self.tiles.append([])
            for y in range(tiles_per_col):
                t = Tile(x, y, self.tile_width, self.tile_height)
                t.set(self.blank, 0, 0)
                self.tiles[x].append(t)

class TextureCache(object):
    def __init__(self):
        self.cache = {}

    def get(self, filename):
        if filename not in self.cache:
            self.cache[filename] = pygame.image.load(filename)
        return self.cache[filename]

class Tile(object):
    def __init__(self, x, y, width, height):
        self.texture = None
        self.dest = pygame.Rect(x*width, y*height, width, height)
        self.width = width
        self.height = height

    def set(self, texture, tile_x, tile_y):
        self.texture = texture
        self.src = pygame.Rect(tile_x*self.width, tile_y*self.height,
                               self.width, self.height)

    def draw(self, screen):
        screen.blit(self.texture, self.dest, self.src)

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
        self.src = pygame.Rect(0, 0, 0, 0)
        self.dest = pygame.Rect(0, 0, 0, 0)
        self.set_animation(list(self.sprite.animations.keys())[0])

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

    def draw(self, screen, delta):
        self._animate(delta)
        if self.current_animation != None and self.visible and self.current_frame[0] != -1:
            screen.blit(self.texture, self.dest, self.src)

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
