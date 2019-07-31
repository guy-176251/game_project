import pygame
from const import *
from utils import *
from sprites import *
from pygame.locals import *
from level import Level

def main():

    pygame.init()
    pygame.display.set_caption('Totally not MegaMan')

    bg     = pygame.Surface(SCREEN_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    fps    = pygame.time.Clock()

    shot_img   = pygame.image.load('images/shot.png').convert_alpha()
    splash_img = pygame.image.load('images/splash.png').convert_alpha()
    enemy_img  = {
        d: [pygame.image.load(f'images/enemy/{d}/{n + 1}.png').convert_alpha()
            for n in range(4)]
        for d in (FWD, BACK)

    }

    bg.fill((0,0,0))

    player = Player(screen=screen)
    all_shots = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    with open('map/dimensions.txt', 'r') as f:
        walls = [eval(f'({r})') for r in f.read().split('\n')[1:] if r != '']
    with open('map/grid.txt', 'r') as f:
        grid = List([List(eval(f'[{l}]')) for l in f.read().split('\n') if l != ''])

    level = Level(
        image = 'map/image.png',
        player = player,
        display = screen,
        walls = walls,
        grid = grid,
        shots =all_shots
    )

    pygame.time.set_timer(ANIMATE, 120)

    # splash loop
    splash_running = True
    while splash_running:
        fps.tick(30)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                splash_running = False
        screen.blit(level.image, (0,0))
        screen.blit(splash_img, (0,0))
        pygame.display.flip()

    # game loop
    game_running = True
    while game_running:
        fps.tick(60)

        level.move(pygame.key.get_pressed())
        all_shots.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_running = False

            elif event.type == QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                all_shots.add(Shot(shot_img, player, SCREEN_SIZE[0]))
                player.buster = BUSTER

            #elif event.type == ticks['animate'][0]:
            elif event.type == ANIMATE:
                all_sprites.update()

        screen.blit(bg, (0,0))
        screen.blit(level.image, level.rect)

        #temp_walls = []
        #for wall in level.walls:
        #    surf = pygame.Surface((wall.w, wall.h))
        #    surf.fill((0,0,255))
        #    temp_walls.append((surf, wall))
        #screen.blits(temp_walls)

        screen.blit(player.image, player.img_point)
        screen.blits((spr.image, spr.rect) for spr in all_shots)

        pygame.display.flip()

    print(level.test_grid)
    print(level.test_coordinates)

main()
