import sys

sys.path.append("../src")

import ewarg, pygame

pygame.init()

ewarg = ewarg.ewarg()

ewarg.init(320, 256)

running = True

red = 0
red_dx = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    red += red_dx
    if red == 255 or red == 0:
        red_dx = -red_dx
    ewarg.set_bg_color(red, 0, 0)
    ewarg.redraw()

pygame.display.quit()
pygame.quit()
