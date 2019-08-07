import pygame
from const import *
from pygame.locals import *

class Shot(pygame.sprite.Sprite):
    def __init__(self, img, player, screen_width):
        super().__init__()
        self.image = img
        self.rect: pygame.Rect = self.image.get_rect()
        self.fwd   = player.fwd
        self.screen_width = screen_width

        if self.fwd == FWD:
            self.rect.midleft = (player.rect.midright[0] + player.width_gap,
                                 player.rect.midright[1])
        else:
            self.rect.midright = (player.rect.midleft[0] - player.width_gap,
                                  player.rect.midleft[1])

        if not player.if_falling:
            self.rect.y += 8
        else:
            self.rect.y -= 8

        self.rect.y -= player.height_gap

        self.speed = 10

    def update(self, y = None):
        if y == None:
            if self.fwd == FWD:
                self.rect.x += self.speed
                if self.rect.right > self.screen_width:
                    self.kill()
            else:
                self.rect.x -= self.speed
                if self.rect.left < 0:
                    self.kill()
        else:
            self.rect.move_ip(0, y)

class Enemy(pygame.sprite.Sprite):

    speed = 2

    def __init__(self, images, player, platform, walls, shots, display, midbottom):
        super().__init__()
        self.images = images
        self.display = display
        self.player = player
        self.walls = walls
        self.shots = shots
        self.platform: pygame.Rect = platform
        self.midbottom = list(midbottom)

        if self.player.rect.x < self.midbottom[0]:
            self.fwd = BACK
        else:
            self.fwd = FWD

        self.image = self.images[self.fwd][0]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midbottom = self.midbottom

        self.max_wait_tick = 100
        self.wait_tick = 0

        self.max_walk_tick = 100
        self.walk_tick = 0

        self.if_moving = False

        self.walk_ind = 0

    @property
    def step(self):
        if self.fwd == FWD:
            return self.speed
        else:
            return self.speed * -1

    def update(self, animate = False, x = 0, y = 0):

        if pygame.sprite.spritecollide(self, self.shots, True):
            self.kill()
            return

        if x or y:
            self.move(x, y)
            return

        if animate:
            self.animate()
            return

        if self.wait_tick == self.max_wait_tick:
            if self.walk_tick < self.max_walk_tick:
                self.walk()
                self.walk_tick += 1
                self.if_moving = True
            else:
                self.if_moving = False
                self.wait_tick = 0
                self.walk_tick = 0
        else:
            self.wait_tick += 1

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.midbottom[0] += x
        self.midbottom[1] += y

    def animate(self):
        if self.if_moving:
            self.image = self.images[self.fwd][self.walk_ind + 2]

            if self.walk_ind:
                self.walk_ind -= 1
            else:
                self.walk_ind += 1

        else:
            self.image = self.images[self.fwd][1]

        # change image
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.midbottom

    def walk(self):
        self.rect.x += self.step

        if self.rect.collidelistall(self.walls):
            wall = self.walls[self.rect.collidelistall(self.walls)[0]]

            if self.fwd == FWD:
                self.rect.right = wall.left
                self.fwd = BACK
            else:
                self.rect.left = wall.right
                self.fwd = FWD

        if self.rect.right > self.platform.right and self.fwd == FWD:
            self.rect.right = self.platform.right
            self.fwd = BACK
        elif self.rect.left < self.platform.left and self.fwd == BACK:
            self.rect.left = self.platform.left
            self.fwd = FWD

        self.midbottom[0] += self.step

class Player(pygame.sprite.Sprite):
    def __init__(self, *, walls = None, screen = None):
        super().__init__()

        self.imgs = {
            img: {
                d: {
                    m: pygame.image.load(f'images/player/{img}/{d}/{m}/1.png').convert_alpha()
                    for m in (BUSTER, NONE)
                }
                for d in (FWD, BACK)
            }
            for img in (RUN, JUMP, STAND)
        }

        self.imgs[RUNNING] = {
            d: {
                m: [pygame.image.load(f'images/player/run/{d}/{m}/{n}.png').convert_alpha() for n in (2,3,4)]
                for m in (BUSTER, NONE)
            }
            for d in (FWD, BACK)
        }

        self.imgs[CLIMB] = {
            NONE: [pygame.image.load(f'images/player/climb/none/{n}.png').convert_alpha() for n in (1,2)],
            BUSTER: {
                d: pygame.image.load(f'images/player/climb/buster/{d}/1.png')
                for d in (FWD, BACK)
            }
        }

        self.climb_ind = 0

        self.run_ind   = 0
        self.run_cycle = True

        self.fwd         = FWD
        self.buster      = NONE
        self.if_moving   = False
        self.if_falling  = False
        self.if_running  = False
        self.if_climbing = False

        self.image  = self.imgs[STAND][FWD][NONE]
        self.rect: pygame.Rect = self.image.get_rect()
        self.walls  = walls
        self.screen = screen

        self.rect.center = (self.screen.get_rect().centerx, 0)

        self.jump_tick     = 0
        self.jump_steps    = [n**2 for n in range(9, 0, -1)]
        self.max_jump_tick = len(self.jump_steps)

        self.rect.width = 30
        self.rect.height = 60
        self.width_gap = int((64 - self.rect.width) / 2)
        self.height_gap = 64 - self.rect.height

        self.change_x   = 0
        self.change_y   = 0

    @property
    def img_point(self):
        return (self.rect.x - self.width_gap, self.rect.y - self.height_gap)

    def update(self):

        if self.if_climbing:
            if self.buster == NONE:
                self.image = self.imgs[CLIMB][NONE][self.climb_ind]

                if self.climb_ind:
                    self.climb_ind -= 1
                else:
                    self.climb_ind += 1

            else:
                self.image = self.imgs[CLIMB][BUSTER][self.fwd]

        elif self.if_falling:
            self.image = self.imgs[JUMP][self.fwd][self.buster]

        elif self.if_moving:

            if not self.if_running:
                self.image = self.imgs[RUN][self.fwd][self.buster]
                self.if_running = True
            else:
                self.image = self.imgs[RUNNING][self.fwd][self.buster][self.run_ind]

                if self.run_cycle:
                    self.run_ind += 1
                else:
                    self.run_ind -= 1

                if self.run_ind == 2 and self.run_cycle:
                    self.run_cycle = False
                elif self.run_ind == 0 and not self.run_cycle:
                    self.run_cycle = True

        else:
            self.image = self.imgs[STAND][self.fwd][self.buster]
            self.if_running = False

        self.buster  = NONE

    def reset(self):
        self.move(-self.change_x, -self.change_y)

        self.change_x   = 0
        self.change_y   = 0

    def move(self, x, y):
        self.change_x += x
        self.change_y += y

        self.rect.move_ip(x, y)

    def __move_old(self, key_press):
        if key_press[K_SPACE] and self.jump_tick < self.max_jump_tick:
            if not self.if_falling:
                self.rect.move_ip(0, -70)
                self.if_falling = True
            else:
                self.rect.move_ip(0, -3)
            self.jump_tick += 1

            walls_hit = pygame.sprite.spritecollide(self, self.walls, False)

            if walls_hit:
                for wall in walls_hit:
                    self.rect.top = wall.rect.bottom
        else:
            self.rect.move_ip(0, 3)
            walls_hit = pygame.sprite.spritecollide(self, self.walls, False)

            if walls_hit:
                self.if_falling = False
                for wall in walls_hit:
                    self.rect.bottom = wall.rect.top
            else:
                self.if_falling = True

        move = 3 #if self.if_moving else 1

        if key_press[K_d]:
            self.rect.move_ip(move, 0)
            self.if_moving = True
            self.fwd       = FWD
        elif key_press[K_a]:
            self.rect.move_ip(-move, 0)
            self.if_moving = True
            self.fwd       = BACK
        else:
            self.if_moving = False

        walls_hit = pygame.sprite.spritecollide(self, self.walls, False)

        for wall in walls_hit:
            if self.fwd == FWD:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            self.if_falling = False

        if not self.if_falling and not key_press[K_SPACE]:
            self.jump_tick = 0


