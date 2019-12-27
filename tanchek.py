import os
import sys

import pygame as pg

SCREENRECT = pg.Rect(0, 0, 800, 552)
# size = width, height = 1000, 800

main_dir = os.path.split(os.path.abspath(__file__))[0]  # D:\somegame


def load_image(file):
    file = os.path.join(main_dir, "images", file)
    surface = pg.image.load(file)
    return surface.convert()  # convert the Surface to the same pixel format as the one you use for final display;
    # it's about the speed of pixel conversion


class Tanchek(pg.sprite.Sprite):
    speed = 1
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.facing = 1

    def move(self, direction):
        self.facing = direction
        if direction == 1:
            self.image = self.images[0]
            self.rect.move_ip(0, -self.speed)
        elif direction == 2:
            self.image = self.images[1]
            self.rect.move_ip(self.speed, 0)
        elif direction == 3:
            self.image = self.images[2]
            self.rect.move_ip(0, self.speed)
        elif direction == 4:
            self.image = self.images[3]
            self.rect.move_ip(-self.speed, 0)


def main():
    pg.init()
    screen = pg.display.set_mode(SCREENRECT.size)

    img = load_image("tanchek.png")
    Tanchek.images = [img, pg.transform.rotate(img, -90), pg.transform.rotate(img, 180), pg.transform.rotate(img, 90)]

    back_piece = load_image("back.png")
    background = pg.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, back_piece.get_width()):
        background.blit(back_piece, (x, 0))  # draws backPiece onto background
    screen.blit(background, (0, 0))
    pg.display.flip()
    # screen.fill(0, 30, 0)
    # pg.display.flip()

    all = pg.sprite.RenderUpdates()
    Tanchek.containers = all

    clock = pg.time.Clock()

    tanchek = Tanchek()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        keystate = pg.key.get_pressed()

        all.clear(screen, background)
        all.update()

        if keystate[pg.K_w]:
            tanchek.move(1)
        elif keystate[pg.K_d]:
            tanchek.move(2)
        elif keystate[pg.K_a]:
            tanchek.move(4)
        elif keystate[pg.K_s]:
            tanchek.move(3)

        dirty = all.draw(screen)
        pg.display.update(dirty)

        clock.tick(40)


if __name__ == "__main__":
    main()
