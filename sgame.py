import os
import pygame
import sys

pygame.init()

size = width, height = 1000, 800
backColor = 0, 30, 0

screen = pygame.display.set_mode(size)

tanchek = pygame.image.load("images/tanchek2.png")
tanchekRect = tanchek.get_rect(topleft=(width / 2, height / 2))

velocity_y = 0
velocity_x = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                velocity_y -= 1
            elif event.key == pygame.K_s:
                velocity_y += 1
            elif event.key == pygame.K_a:
                velocity_x -= 1
            elif event.key == pygame.K_d:
                velocity_x += 1
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_w or event.key == pygame.K_s) and velocity_y != 0:
                velocity_y = 0
            if (event.key == pygame.K_a or event.key == pygame.K_d) and velocity_x != 0:
                velocity_x = 0

    tanchekRect.centery += velocity_y
    tanchekRect.centerx += velocity_x

    screen.fill(backColor)
    screen.blit(tanchek, tanchekRect)
    pygame.display.flip()