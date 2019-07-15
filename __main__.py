import pygame
from const import *
from sprites import *
from pygame.locals import *

def main():
    pygame.init()
    pygame.display.set_caption('Totally not MegaMan')

    screen = pygame.display.set_mode((800, 600))
    bg     = pygame.image.load('bg.jpg').convert()

    player = Player()
    #walls  = pygame.sprite.Group(Wall((200, 10), 400, 445))
    walls  = pygame.sprite.Group(Wall('platform.png', 400, 445))
    player.walls = walls

    all_sprites = pygame.sprite.Group(player, walls)

    ANIM_TICK = pygame.USEREVENT + 1
    pygame.time.set_timer(ANIM_TICK, 100)

    MOVE_TICK = pygame.USEREVENT + 2
    pygame.time.set_timer(MOVE_TICK, 10)

    while True:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            elif event.type == QUIT:
                return
            elif event.type == MOVE_TICK:
                player.move(pygame.key.get_pressed())
            elif event.type == ANIM_TICK:
                player.animate()

        screen.blit(bg, (0,0))
        screen.blits((spr.image, spr.rect) for spr in all_sprites)

        pygame.display.flip()

main()
