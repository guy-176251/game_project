import pygame
from const import *
from utils import *
from pygame.locals import *

class Level(pygame.sprite.Sprite):
    def __init__(self, *, image: str,
                          walls: list,
                          grid: list,
                          ladders: list,
                          traps: list,
                          display: pygame.Surface,
                          player: pygame.sprite.Sprite,
                          shots: pygame.sprite.Group):

        self.image = pygame.image.load(image).convert_alpha()

        self.rect   : pygame.Rect    = self.image.get_rect()
        self.display: pygame.Surface = display

        self.walls   = [pygame.Rect(*w) for w in walls]
        self.ladders = [pygame.Rect(*l) for l in ladders]
        self.traps   = [pygame.Rect(*t) for t in traps]
        self.grid    = grid
        self.t_grid  = [[0 for _ in range(len(self.grid[0]))]
                        for _ in range(len(self.grid))]

        self.t_coordinates = set()
        self.player        = player
        self.shots         = shots

        self.if_dead  = False
        self.change_x = 0
        self.change_y = 0

    def reset(self):
        self.move_all(-self.change_x, -self.change_y)

        self.change_x   = 0
        self.change_y   = 0

    def move_all(self, x, y):
        self.change_x += x
        self.change_y += y

        self.rect.move_ip(x, y)
        for wall in self.walls:
            wall.move_ip(x, y)
        for trap in self.traps:
            trap.move_ip(x, y)
        for ladder in self.ladders:
            ladder.move_ip(x, y)
        self.shots.update(y)

    @property
    def debug_info(self):
        return '\n' + '\n'.join(' '.join(str(n) for n in row) for row in self.t_grid) + '\n\n' + '\n'.join(sorted(list(self.t_coordinates)))

    @property
    def x(self):
        return int((self.rect.x * -1 + self.player.rect.centerx) / self.display.get_width())

    @property
    def y(self):
        return int((self.rect.y * -1 + self.player.rect.centery) / self.display.get_height())

    def move(self, key_press):
        if key_press[K_SPACE] and self.player.jump_tick < self.player.max_jump_tick and not self.player.if_falling:
            self.player.move(0, -self.player.jump_steps[self.player.jump_tick])
            self.player.jump_tick += 1

            walls_hit = [w for w in self.walls if self.player.rect.colliderect(w)]

            if walls_hit:
                self.player.if_falling = True
                for wall in walls_hit:
                    self.player.move(0, -self.player.rect.top + wall.bottom)

            if All(self.player.rect.centery <= 0,
                   self.y > 0,
                   self.grid[sub(self.y, 1)][self.x]):

                self.move_all(0, self.display.get_height())
                self.player.move(0, self.display.get_height())

        else:
            self.player.if_falling = True
            self.player.move(0, 6)
            walls_hit = [w for w in self.walls if self.player.rect.colliderect(w)]

            if walls_hit:
                self.player.if_falling = False
                for wall in walls_hit:
                    self.player.move(0, -self.player.rect.bottom + wall.top)
            else:
                self.player.jump_tick = self.player.max_jump_tick

            if self.player.rect.centery >= self.display.get_height():
                self.t_coordinates.add(f'grid {self.x}, {self.y}: {self.grid[self.y][self.x]}')

            if All(self.player.rect.centery >= self.display.get_height(),
                   self.grid[self.y][self.x]):

                self.move_all(0, -self.display.get_height())
                self.player.move(0, -self.display.get_height())

        move = 3 if self.player.if_moving else 1

        if key_press[K_d]:
            self.player.move(move, 0)
            self.player.if_moving = True
            self.player.fwd       = FWD

            if All(self.rect.x * -1 > self.display.get_width(),

                   Any(self.grid[self.y + 1][self.x],
                       self.grid[sub(self.y, 1)][self.x]),

                   self.rect.x % self.display.get_width() != 0):

                #print('x', self.x)
                diff = self.rect.x % self.display.get_width()
                #print('before', self.rect.x)
                #print('diff', diff)
                self.move_all(-diff, 0)
                self.player.move(-diff, 0)
                #print('after', self.rect.x, '\n')

            elif All(self.player.rect.centerx > self.display.get_rect().centerx,
                     self.grid[self.y][self.x + 1],
                     not self.grid[self.y + 1][self.x],
                     not self.grid[sub(self.y, 1)][self.x]):

                diff = self.player.rect.centerx - self.display.get_rect().centerx
                self.player.move(-diff, 0)
                self.move_all(-diff, 0)

        elif key_press[K_a]:
            self.player.move(-move, 0)
            self.player.if_moving = True
            self.player.fwd       = BACK

            if All(self.rect.x * -1 > self.display.get_width(),

                   Any(self.grid[self.y + 1][self.x],
                       self.grid[sub(self.y, 1)][self.x]),

                   self.rect.x % self.display.get_width() != 0):

                diff = self.rect.x % self.display.get_width()
                #print('x', self.x)
                #print('before', self.rect.x)
                #print('diff', diff)
                self.move_all(diff, 0)
                self.player.move(diff, 0)
                #print('after', self.rect.x, '\n')

            elif All(self.player.rect.centerx < self.display.get_rect().centerx,
                     self.rect.x < 0,
                     self.grid[self.y][self.x],
                     not self.grid[self.y + 1][self.x],
                     not self.grid[sub(self.y, 1)][self.x]):

                diff = -self.player.rect.centerx + self.display.get_rect().centerx
                self.player.move(diff, 0)
                self.move_all(diff, 0)

        else:
            self.player.if_moving = False

        if self.player.if_moving:

            walls_hit = [w for w in self.walls if self.player.rect.colliderect(w)]

            for wall in walls_hit:
                if self.player.fwd == FWD:
                    self.player.move(-self.player.rect.right + wall.left, 0)
                else:
                    self.player.move(-self.player.rect.left + wall.right, 0)

        traps_hit = [w for w in self.traps if self.player.rect.colliderect(w)]

        if traps_hit:
            self.if_dead = True

        if not self.player.if_falling and not key_press[K_SPACE]:
            self.player.jump_tick = 0

        self.t_grid[self.y][self.x] = self.grid[self.y][self.x]
