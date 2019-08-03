import pygame
from pygame.locals import *

DEBUG = True

FWD     = 'right'
BACK    = 'left'
DIRS    = (K_a, K_d, K_SPACE)
RUN     = 'run'
JUMP    = 'jump'
STAND   = 'stand'
RUNNING = 'running'
BUSTER  = 'buster'
NONE    = 'none'
ANIMATE = pygame.USEREVENT + 1
SCREEN_SIZE = (512, 448)
