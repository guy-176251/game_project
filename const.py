import pygame
from pygame.locals import *

DEBUG = False

FWD     = 'right'
BACK    = 'left'
DIRS    = (K_a, K_d, K_SPACE)
RUN     = 'run'
JUMP    = 'jump'
STAND   = 'stand'
RUNNING = 'running'
BUSTER  = 'buster'
NONE    = 'none'
CLIMB   = 'climb'
ANIMATE = pygame.USEREVENT + 1
SPAWN   = pygame.USEREVENT + 2
SCREEN_SIZE = (512, 448)
ENEMY_WIDTH = 36
TOP     = 'top'
BOTTOM  = 'bottom'
