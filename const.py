from pygame.locals import *

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

FLOOR   = 425
FWD     = 'right'
BACK    = 'left'
GRAV    = 5
DIRS    = (K_a, K_d)
RUN     = 'run'
JUMP    = 'jump'
STAND   = 'stand'
RUNNING = 'running'
ACTIONS = (RUN, JUMP, STAND)
KEY_DIR = {False: BACK, True: FWD}
