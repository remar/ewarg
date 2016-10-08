import sys

sys.path.append("../src")

import ewarg, sdl2, sdl2.ext, random, math

sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

ewarg = ewarg.ewarg()

WIDTH = 32*10
HEIGHT = 32*8

ewarg.init(WIDTH, HEIGHT)
ewarg.set_tilesize(32, 32)
ewarg.load_tileset("block", "data/block1.bmp")
ewarg.load_sprite("data/fuzz.json")

row = math.ceil(WIDTH / 32)
col = math.ceil(HEIGHT / 32)

for y in range(1, col - 1):
    ewarg.set_tile(0, y, "block", 2, 0)
    ewarg.set_tile(row - 1, y, "block", 2, 0)

for x in range(1, row - 1):
    ewarg.set_tile(x, 0, "block", 1, 0)
    ewarg.set_tile(x, col - 1, "block", 1, 0)

ewarg.set_tile(0, 0, "block", 3, 0)
ewarg.set_tile(row - 1, 0, "block", 4, 0)
ewarg.set_tile(0, col - 1, "block", 5, 0)
ewarg.set_tile(row - 1, col - 1, "block", 6, 0)

class Fuzz(object):
    def __init__(self, ewarg):
        self.ewarg = ewarg
        self.sprite_id = ewarg.create_sprite_instance("fuzz")
        self.x = random.randint(33, WIDTH-32-24-1)
        self.y = random.randint(33, HEIGHT-32-24-1)
        self.dx = -1 if random.randint(0, 1) == 0 else +1
        self.dy = -1 if random.randint(0, 1) == 0 else +1
        self.rolling_left = True if random.randint(0, 1) == 0 else False
        self.update_animation()
        ewarg.move_sprite_abs(self.sprite_id, self.x, self.y)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x == 32 or self.x == WIDTH-32-24:
            self.dx = -self.dx
            self.toggle_direction()
        if self.y == 32 or self.y == HEIGHT-32-24:
            self.dy = -self.dy
            self.toggle_direction()

        ewarg.move_sprite_abs(self.sprite_id, self.x, self.y)

    def remove(self):
        self.ewarg.remove_sprite_instance(self.sprite_id)

    def toggle_direction(self):
        self.rolling_left = not self.rolling_left
        self.update_animation()

    def update_animation(self):
        ewarg.set_animation(self.sprite_id,
                            "roll left" if self.rolling_left else "roll right")

fuzzes = []
for i in range(10):
    fuzzes.append(Fuzz(ewarg))

running = True

while running:
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.scancode == sdl2.SDL_SCANCODE_Q:
                running = False
                break
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_SPACE:
                for i in range(10):
                    fuzzes.append(Fuzz(ewarg))
                print("Number of fuzzies:", len(fuzzes))
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_C:
                for fuzz in fuzzes[10:]:
                    fuzz.remove()
                fuzzes = fuzzes[:10]

    for fuzz in fuzzes:
        fuzz.move()

    ewarg.redraw()

sdl2.SDL_Quit()
