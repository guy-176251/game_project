import os
import pygame
from const import *
from utils import *
from sprites import *
from pygame.locals import *
from level import Level

def main():

    if any(folder not in os.listdir() for folder in ('images', 'map', 'sounds')):
        try:
            os.chdir('game_project')
        except:
            print('The main folder/file name needs to be called "game_project" for the game to run.')
            return

    pygame.mixer.pre_init()
    pygame.init()
    pygame.display.set_caption('MegaMan: Pump Man Stage')

    pygame.mixer.music.load('sounds/level.mp3')
    pygame.mixer.music.play(-1)

    bg     = pygame.Surface(SCREEN_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    fps    = pygame.time.Clock()

    shot_img   = pygame.image.load('images/shot.png').convert_alpha()
    death_img = pygame.image.load('images/death.png').convert_alpha()
    splash_img = pygame.image.load('images/splash.png').convert_alpha()
    instructions_img = pygame.image.load('images/instructions.png').convert_alpha()
    enemy_img  = {
        d: [pygame.image.load(f'images/enemy/{d}/{n + 1}.png').convert_alpha()
            for n in range(4)]
        for d in (FWD, BACK)

    }

    bg.fill((0,0,0))

    player = Player(screen=screen)
    all_shots = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    with open('map/walls.txt', 'r') as f:
        walls = [eval(f'({r})') for r in f.read().split('\n')[1:] if r != '']
    with open('map/traps.txt', 'r') as f:
        traps = [eval(f'({r})') for r in f.read().split('\n') if r != '']
    with open('map/ladders.txt', 'r') as f:
        ladders = [eval(f'({r})') for r in f.read().split('\n') if r != '']
    with open('map/grid.txt', 'r') as f:
        grid = List([List(eval(f'[{l}]')) for l in f.read().split('\n') if l != ''])

    level = Level(
        image = 'map/image.png',
        player = player,
        display = screen,
        walls = walls,
        ladders=ladders,
        traps=traps,
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

    # shows key controls
    instructions_running = True
    while instructions_running:
        fps.tick(30)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                instructions_running = False
        screen.blit(level.image, (0,0))
        screen.blit(instructions_img, (0,0))
        pygame.display.flip()

    # game loop
    game_running = True
    while game_running:

        while not level.if_dead:
            fps.tick(60)
            level.move(pygame.key.get_pressed())
            all_shots.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    game_running = False
                    return level.debug_info

                elif event.type == QUIT:
                    game_running = False
                    return level.debug_info

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    all_shots.add(Shot(shot_img, player, SCREEN_SIZE[0]))
                    player.buster = BUSTER

                elif event.type == ANIMATE:
                    all_sprites.update()

            screen.blit(bg, (0,0))
            screen.blit(level.image, level.rect)

            if DEBUG:
                temp_walls = []
                for wall in level.walls:
                    surf = pygame.Surface((wall.w, wall.h))
                    surf.fill((0,0,255))
                    temp_walls.append((surf, wall))
                for trap in level.traps:
                    surf = pygame.Surface((trap.w, trap.h))
                    surf.fill((255,0,0))
                    temp_walls.append((surf, trap))
                for ladder in level.ladders:
                    surf = pygame.Surface((ladder.w, ladder.h))
                    surf.fill((0,255,0))
                    temp_walls.append((surf, ladder))
                screen.blits(temp_walls)

            screen.blit(player.image, player.img_point)
            screen.blits((spr.image, spr.rect) for spr in all_shots)

            if DEBUG:
                pygame.display.set_caption(f'{int(fps.get_fps())} FPS; {level.x}, {level.y}')
            else:
                pygame.display.set_caption(f'{int(fps.get_fps())} FPS')

            pygame.display.flip()

        death_screen = True
        while death_screen:
            fps.tick(30)
            screen.blit(bg, (0,0))
            screen.blit(level.image, level.rect)
            screen.blit(death_img, (0,0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    level.reset()
                    player.reset()
                    death_screen = False
                    level.if_dead = False


if DEBUG:
    print(main())
else:
    main()
