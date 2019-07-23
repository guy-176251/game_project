import pygame
from const import *
from sprites import *
from pygame.locals import *

def main():

    pygame.init()
    pygame.display.set_caption('Totally not MegaMan')

    screen = pygame.display.set_mode((800, 600))
    fps    = pygame.time.Clock()

    bg     = pygame.image.load('bg.jpg').convert()
    shot   = pygame.image.load('shot.png').convert_alpha()
    splash = pygame.image.load('splash.png').convert_alpha()

    level = [
        [('platform.png', 400, 445)]
    ]

    walls  = Walls(level[0])
    player = Player(walls = walls, screen = screen)

    all_sprites = pygame.sprite.Group(player, walls)
    all_shots   = pygame.sprite.Group()

    ticks = {
        'animate': (pygame.USEREVENT + 1, 100),
        #'move'   : (pygame.USEREVENT + 2, 10)
    }

    for t in ticks:
        pygame.time.set_timer(*ticks[t])

    # splash loop
    splash_running = True
    while splash_running:
        fps.tick(30)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                splash_running = False
        screen.blit(bg, (0,0))
        screen.blit(splash, (0,0))
        pygame.display.flip()

    # game loop
    game_running = True
    while game_running:
        fps.tick(60)

        player.move(pygame.key.get_pressed())
        all_shots.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_running = False

            elif event.type == QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                all_shots.add(Shot(shot, player))
                player.buster = BUSTER

            #elif event.type == ticks['move'][0]:
            #    player.move(pygame.key.get_pressed())
            #    all_shots.update()

            elif event.type == ticks['animate'][0]:
                all_sprites.update()

        screen.blit(bg, (0,0))
        screen.blits((spr.image, spr.rect) for spr in all_sprites)
        screen.blits((spr.image, spr.rect) for spr in all_shots)

        pygame.display.flip()

main()
