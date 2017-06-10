import sys

sys.path.append("../src")

import ewarg, pygame

pygame.init()

ewarg = ewarg.ewarg()

ewarg.init(320, 256)
ewarg.set_tilesize(32, 32)
ewarg.load_tileset("block", "data/block1.bmp")

for y in range(4):
    for x in range(5):
        ewarg.set_tile(x*2, y*2, "block", 3, 0)
        ewarg.set_tile(x*2+1, y*2, "block", 4, 0)
        ewarg.set_tile(x*2, y*2+1, "block", 5, 0)
        ewarg.set_tile(x*2+1, y*2+1, "block", 6, 0)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    ewarg.redraw()

pygame.display.quit()
pygame.quit()
