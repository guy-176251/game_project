import pygame
from const import *
from sprites import *
from pygame.locals import *

def main():

    pygame.init()
    pygame.display.set_caption('Totally not MegaMan')

    screen = pygame.display.set_mode((800, 600))
    bg     = pygame.image.load('bg.jpg').convert()
    shot   = pygame.image.load('shot.png').convert_alpha()

    wall_groups = [
        [('platform.png', 400, 445)]
    ]

    level = {
        ind + 1: [Wall(*dim) for dim in lvl]
        for ind, lvl in enumerate(wall_groups)
    }

    walls  = pygame.sprite.Group(level[1])
    player = Player(walls = walls, screen = screen)

    all_sprites = pygame.sprite.Group(player, walls)
    all_shots   = pygame.sprite.Group()

    ticks = {
        'animate': (pygame.USEREVENT + 1, 100),
        'move'   : (pygame.USEREVENT + 2, 10)
    }

    for t in ticks:
        pygame.time.set_timer(*ticks[t])

    while True:

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            elif event.type == QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                all_shots.add(Shot(shot, player))
                player.buster = BUSTER

            elif event.type == ticks['move'][0]:
                player.move(pygame.key.get_pressed())
                all_shots.update()

            elif event.type == ticks['animate'][0]:
                all_sprites.update()

        screen.blit(bg, (0,0))
        screen.blits((spr.image, spr.rect) for spr in all_sprites)
        screen.blits((spr.image, spr.rect) for spr in all_shots)

        pygame.display.flip()

main()
