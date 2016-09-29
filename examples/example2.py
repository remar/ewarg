import sys

sys.path.append("../src")

import ewarg, sdl2, sdl2.ext

sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

ewarg = ewarg.ewarg()

ewarg.init(320, 256)
ewarg.set_tilesize(32, 32)
ewarg.load_tileset("block", "data/block1.bmp")
ewarg.load_sprite("data/cpngood.json")

cpn_good_id = ewarg.create_sprite_instance("cpngood")

ewarg.set_animation(cpn_good_id, "walk right")
ewarg.move_sprite_abs(cpn_good_id, 0, 64*3 - 24)

cpn_good_x = 0
cpn_good_dx = +1

for y in range(4):
    if y == 2:
        continue
    for x in range(5):
        ewarg.set_tile(x*2, y*2, "block", 3, 0)
        ewarg.set_tile(x*2+1, y*2, "block", 4, 0)
        ewarg.set_tile(x*2, y*2+1, "block", 5, 0)
        ewarg.set_tile(x*2+1, y*2+1, "block", 6, 0)

running = True

while running:
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_QUIT:
            running = False
            break

    cpn_good_x += cpn_good_dx
    if cpn_good_x == 0 or cpn_good_x == 320-16:
        cpn_good_dx = -cpn_good_dx
        ewarg.set_animation(cpn_good_id, "walk right" if cpn_good_dx == 1 else "walk left")
    ewarg.move_sprite_abs(cpn_good_id, cpn_good_x, 64*3 - 24)

    ewarg.redraw()

sdl2.SDL_Quit()
