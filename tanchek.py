import os
import sys
import random

import pygame as pg

SCREENRECT = pg.Rect(0, 0, 800, 552)
# size = width, height = 1000, 800
MAX_SHOTS = 10
MAX_OBSTACLES = 3

main_dir = os.path.split(os.path.abspath(__file__))[0]  # D:\somegame


def load_image(file):
    file = os.path.join(main_dir, "images", file)
    surface = pg.image.load(file)
    return surface.convert()  # convert the Surface to the same pixel format as the one you use for final display;
    # it's about the speed of pixel conversion


class Tanchek(pg.sprite.Sprite):
    # speed = 4
    images = []

    speed_up = 4
    speed_down = 4
    speed_right = 4
    speed_left = 4

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.surface = self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.facing = 1
        self.direction = self.facing
        self.reloading = 0
        self.blocks = None

    def move(self, direction):
        self.facing = direction
        self.surface = self.image.set_colorkey((255, 255, 255))
        if direction == 1:
            self.image = self.images[0]
            self.rect.move_ip(0, -self.speed_up)
        elif direction == 2:
            self.image = self.images[1]
            self.rect.move_ip(self.speed_right, 0)
        elif direction == 3:
            self.image = self.images[2]
            self.rect.move_ip(0, self.speed_down)
        elif direction == 4:
            self.image = self.images[3]
            self.rect.move_ip(-self.speed_left, 0)

    def update(self):

        block_hit_list = pg.sprite.spritecollide(self, self.blocks, False)
        for block in block_hit_list:
            if self.rect.top in range(block.rect.bottom - 5, block.rect.bottom + 5):
                self.speed_up = 0
            elif self.rect.bottom in range(block.rect.top - 5, block.rect.top + 5):
                self.speed_down = 0
            elif self.rect.right in range(block.rect.left - 5, block.rect.left + 5):
                self.speed_right = 0
            elif self.rect.left in range(block.rect.right - 5, block.rect.right + 5):
                self.speed_left = 0
        if not block_hit_list:
            self.speed_up = 4
            self.speed_down = 4
            self.speed_right = 4
            self.speed_left = 4


class Ammo(pg.sprite.Sprite):
    speed = 5
    direction = 1
    images = []

    def __init__(self, pos, direction):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.surface = self.image.set_colorkey((255, 255, 255))
        # self.rect = self.image.get_rect(center=(pos_x, pos_y)) why does it not fucking work???

    def update(self):

        # self.rect.move_ip(self.direction, self.speed)
        self.surface = self.image.set_colorkey((255, 255, 255))
        if self.direction == 1:
            self.image = self.images[0]
            self.rect.move_ip(0, -self.speed)
        elif self.direction == 2:
            self.image = self.images[1]
            self.rect.move_ip(self.speed, 0)
        elif self.direction == 3:
            self.image = self.images[2]
            self.rect.move_ip(0, self.speed)
        elif self.direction == 4:
            self.image = self.images[3]
            self.rect.move_ip(-self.speed, 0)

        if self.rect.top <= 0 or self.rect.bottom >= 552 or self.rect.left <= 0 or self.rect.right >= 800:
            self.kill()


class Obstacle(pg.sprite.Sprite):
    images = []
    collide_counter = 0

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.surface = self.image.set_colorkey((255, 255, 255))

    def update(self):
        self.surface = self.image.set_colorkey((255, 255, 255))


class Explosion(pg.sprite.Sprite):
    images = []
    defaultlife = 10

    def __init__(self, actor):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.surface = self.image.set_colorkey((255, 255, 255))
        self.life = self.defaultlife

    def update(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()


def main():
    pg.init()
    screen = pg.display.set_mode(SCREENRECT.size)

    img = load_image("tanchek.png")
    Tanchek.images = [img, pg.transform.rotate(img, -90), pg.transform.rotate(img, 180), pg.transform.rotate(img, 90)]
    img = load_image("ammo.png")
    Ammo.images = [img, pg.transform.rotate(img, -90), pg.transform.rotate(img, 180), pg.transform.rotate(img, 90)]
    img = load_image("obstacle1.png")
    crashed_img = load_image("obstacle2.png")
    Obstacle.images = [img, crashed_img]
    img = load_image("explosion.png")
    Explosion.images = [img]

    #back_piece = load_image("back3.png")
    #background = pg.Surface(SCREENRECT.size)
    #for x in range(0, SCREENRECT.width, back_piece.get_width()):
    #    background.blit(back_piece, (x, 0))  # draws backPiece onto background
    background = load_image("back3.png")
    screen.blit(background, (0, 0))
    pg.display.flip()
    # screen.fill(back_color)
    # pg.display.flip()

    ammos = pg.sprite.Group()
    obstacles = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()

    Tanchek.containers = all
    Ammo.containers = ammos, all
    Obstacle.containers = obstacles, all
    Explosion.containers = all

    clock = pg.time.Clock()

    #tanchek = Tanchek()
    #tanchek.blocks = obstacles

    obstacle_cycle = 0
    i = 100
    while obstacle_cycle < MAX_OBSTACLES:
        Obstacle(random.randint(i, i + SCREENRECT.width // 5), random.randint(20, SCREENRECT.height - SCREENRECT.height // 3))
        i += 80 + SCREENRECT.width // 5
        obstacle_cycle += 1

    tanchek = Tanchek()
    tanchek.blocks = obstacles

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

        firing = keystate[pg.K_SPACE]
        if not tanchek.reloading and firing and len(ammos) < MAX_SHOTS:
            Ammo(tanchek.rect.center, tanchek.facing)
        tanchek.reloading = firing

        for obstacle in pg.sprite.groupcollide(obstacles, ammos, 0, 1):
            Explosion(obstacle)
            obstacle.collide_counter += 1
            if obstacle.collide_counter == 3:
                obstacle.image = Obstacle.images[1]
            elif obstacle.collide_counter == 6:
                obstacle.kill()

        dirty = all.draw(screen)
        pg.display.update(dirty)

        clock.tick(40)


if __name__ == "__main__":
    main()
