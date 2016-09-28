import sys

sys.path.append("../src")

import ewarg, sdl2, sdl2.ext, random

ewarg = ewarg.ewarg()

ewarg.init(320, 240)

running = True

while running:
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_QUIT:
            running = False
            break

    ewarg.set_background_color(random.randint(0, 255),
                               random.randint(0, 255),
                               random.randint(0, 255))
    ewarg.redraw()
