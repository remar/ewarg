import sys

sys.path.append("../src")

import ewarg, sdl2, sdl2.ext, random

sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

ewarg = ewarg.ewarg()

ewarg.init(320, 256)
ewarg.set_tilesize(32, 32)
ewarg.load_tileset("block", "data/block1.bmp")
ewarg.load_sprite("data/fuzz.json")

for y in range(1, 7):
    ewarg.set_tile(0, y, "block", 2, 0)
    ewarg.set_tile(9, y, "block", 2, 0)

for x in range(1, 9):
    ewarg.set_tile(x, 0, "block", 1, 0)
    ewarg.set_tile(x, 7, "block", 1, 0)

ewarg.set_tile(0, 0, "block", 3, 0)
ewarg.set_tile(9, 0, "block", 4, 0)
ewarg.set_tile(0, 7, "block", 5, 0)
ewarg.set_tile(9, 7, "block", 6, 0)

class Fuzz(object):
    def __init__(self, ewarg):
        self.ewarg = ewarg
        self.sprite_id = ewarg.create_sprite_instance("fuzz")
        self.x = random.randint(33, 320-32-24-1)
        self.y = random.randint(33, 256-32-24-1)
        self.dx = -1 if random.randint(0, 1) == 0 else +1
        self.dy = -1 if random.randint(0, 1) == 0 else +1
        ewarg.set_animation(self.sprite_id, "roll right")
        ewarg.move_sprite_abs(self.sprite_id, self.x, self.y)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x == 32 or self.x == 320-32-24:
            self.dx = -self.dx
        if self.y == 32 or self.y == 256-32-24:
            self.dy = -self.dy

        ewarg.move_sprite_abs(self.sprite_id, self.x, self.y)

    def remove(self):
        self.ewarg.remove_sprite_instance(self.sprite_id)

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
