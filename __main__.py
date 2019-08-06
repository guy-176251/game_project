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

    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.display.set_caption('MegaMan: Pump Man Stage')

    pygame.mixer.music.load('sounds/level.mp3')
    pygame.mixer.music.play(-1)

    buster_sound = pygame.mixer.Sound('sounds/buster.wav')

    bg     = pygame.Surface(SCREEN_SIZE)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    fps    = pygame.time.Clock()

    bg.fill((0,0,0))

    shot_img = pygame.image.load('images/shot.png').convert_alpha()
    death_img = pygame.image.load('images/death.png').convert_alpha()
    splash_img = pygame.image.load('images/splash.png').convert_alpha()
    instructions_img = pygame.image.load('images/instructions.png').convert_alpha()
    enemy_img  = {
        d: [pygame.image.load(f'images/enemy/{d}/{n + 1}.png').convert_alpha()
            for n in range(4)]
        for d in (FWD, BACK)

    }

    player = Player(screen=screen)
    all_shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    animated_sprites = pygame.sprite.Group(player, enemies)

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
        ladders = ladders,
        traps = traps,
        grid = grid,
        shots = all_shots,
        enemies = enemies,
        enemy_img = enemy_img
    )

    pygame.time.set_timer(ANIMATE, 120)
    pygame.time.set_timer(SPAWN, 250)

    intro = {
        'splash': {'run': True, 'image': splash_img},
        'instructions': {'run': True, 'image': instructions_img}
    }

    for thing in intro:
        imgs = [(level.image, (0,0)), (intro[thing]['image'], (0,0))]
        while intro[thing]['run']:
            fps.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    intro[thing]['run'] = False
            screen.blits(imgs)
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
                    buster_sound.play()

                elif event.type == ANIMATE:
                    animated_sprites.update()

                elif event.type == SPAWN:
                    level.spawn()

            screen.blit(bg, (0,0))
            screen.blit(level.image, level.rect)

            if DEBUG:
                screen.blits(
                    sum([rect_to_surface(r, c)
                         for r, c in ((level.traps,   (255, 0, 0)),
                                      (level.walls,   (0,0,255)),
                                      (level.ladders, (0,255,0)),
                                      (level.ladder_tops, (255,0,255)))],
                        [])
                )

            screen.blit(player.image, player.img_point)
            enemies.draw(screen)
            all_shots.draw(screen)

            if DEBUG:
                pygame.display.set_caption(f'{int(fps.get_fps())} FPS; {level.x}, {level.y}')
            else:
                pygame.display.set_caption(f'{int(fps.get_fps())} FPS')

            pygame.display.flip()

        death_screen = True
        imgs = [(bg, (0,0)), (level.image, level.rect), (death_img, (0,0))]
        while death_screen:
            fps.tick(30)
            screen.blits(imgs)
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
