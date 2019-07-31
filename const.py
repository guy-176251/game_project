import pygame
from pygame.locals import *

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (50, 50, 255)

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
