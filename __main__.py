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

    player = Player()
    #walls  = pygame.sprite.Group(Wall((200, 10), 400, 445))
    walls  = pygame.sprite.Group(Wall('platform.png', 400, 445))
    player.walls = walls

    all_sprites = pygame.sprite.Group(player, walls)
    all_shots   = pygame.sprite.Group()

    ANIM_TICK = pygame.USEREVENT + 1
    pygame.time.set_timer(ANIM_TICK, 100)

    MOVE_TICK = pygame.USEREVENT + 2
    pygame.time.set_timer(MOVE_TICK, 10)

    while True:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                all_shots.add(Shot(shot, player))
                player.if_buster = BUSTER
            elif event.type == QUIT:
                return
            elif event.type == MOVE_TICK:
                player.move(pygame.key.get_pressed())
                all_shots.update()
            elif event.type == ANIM_TICK:
                all_sprites.update()

        screen.blit(bg, (0,0))
        screen.blits((spr.image, spr.rect) for spr in all_sprites)
        screen.blits((spr.image, spr.rect) for spr in all_shots)

        pygame.display.flip()

main()
