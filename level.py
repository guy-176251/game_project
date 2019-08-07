import pygame
from const import *
from utils import *
from sprites import *
from random import choice, randint
from pygame.locals import *

class Level(pygame.sprite.Sprite):
    def __init__(self, *, image: str,
                          walls: list,
                          grid: list,
                          ladders: list,
                          traps: list,
                          spawn_zones: list,
                          display: pygame.Surface,
                          player: pygame.sprite.Sprite,
                          shots: pygame.sprite.Group,
                          enemies: pygame.sprite.Group,
                          enemy_img: dict):

        self.image = pygame.image.load(image).convert_alpha()

        self.rect   : pygame.Rect    = self.image.get_rect()
        self.display: pygame.Surface = display

        self.walls   = [pygame.Rect(*w) for w in walls]
        self.ladders = [pygame.Rect(*l) for l in ladders]
        self.traps   = [pygame.Rect(*t) for t in traps]
        self.spawn_zones = [pygame.Rect(*s) for s in spawn_zones]
        self.ladder_tops = [pygame.Rect(*r.topleft, r.w, 10) for r in self.ladders]
        self.grid    = grid
        self.t_grid  = [[0 for _ in range(len(self.grid[0]))]
                        for _ in range(len(self.grid))]

        self.occupied_walls = []

        self.t_coordinates = set()
        self.player        = player
        self.shots         = shots
        self.enemies       = enemies
        self.enemy_img     = enemy_img

        self.if_dead  = False
        self.if_in_pivot = False
        self.change_x = 0
        self.change_y = 0

        self.enemy_rect: pygame.Rect = self.enemy_img[FWD][3].get_rect()
        self.all_walls = self.walls + self.ladders + self.traps

        self.current_ladder = None

    def reset(self):
        self.move_all(-self.change_x, -self.change_y)

        self.change_x   = 0
        self.change_y   = 0

        self.enemies.empty()
        self.occupied_walls = []

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
        for ladder in self.ladder_tops:
            ladder.move_ip(x, y)
        for s in self.spawn_zones:
            s.move_ip(x,y)
        self.shots.update(y)
        self.enemies.update(False, x,y)

    @property
    def debug_info(self):
        return '\n' + '\n'.join(' '.join(str(n) for n in row) for row in self.t_grid) + '\n\n' + '\n'.join(sorted(list(self.t_coordinates)))

    @property
    def x(self):
        return int((self.rect.x * -1 + self.player.rect.centerx) / self.display.get_width())

    @property
    def y(self):
        return int((self.rect.y * -1 + self.player.rect.centery) / self.display.get_height())

    def spawn(self):
        bound = 100
        spawn_walls = [
            w for w in self.walls
            if All(
                w.width > ENEMY_WIDTH,
                w.width < 200,
                w.width > w.height,
                All(Any(w.right < 0,  w.left > self.display.get_width()),
                    Any(w.bottom < 0, w.top > self.display.get_height())),
                All(Any(w.right >= -bound,
                        w.left <= self.display.get_width() + bound),
                    Any(w.top >= -bound,
                        w.bottom <= self.display.get_height() + bound)),
                w.collidelist(self.spawn_zones),
                w not in self.occupied_walls
                )
        ]

        if spawn_walls:
            wall = choice(spawn_walls)
            self.occupied_walls.append(wall)
            self.enemy_rect.midbottom = wall.midtop

            if not self.enemy_rect.collidelistall(self.all_walls):
                self.enemies.add(Enemy(self.enemy_img,
                                       self.player,
                                       wall,
                                       self.walls,
                                       self.shots,
                                       self.display,
                                       wall.midtop))

    def camera_check(self, mode):
        if mode == TOP:
            if All(self.player.rect.centery <= 0,
                   self.y > 0,
                   self.grid[self.y][self.x]):

                self.move_all(0, self.display.get_height())
                self.player.move(0, self.display.get_height())

        elif mode == BOTTOM:
            if All(self.player.rect.centery >= self.display.get_height(),
                   self.grid[self.y][self.x]):

                self.move_all(0, -self.display.get_height())
                self.player.move(0, -self.display.get_height())

        elif mode == FWD:
            if All(not self.if_in_pivot,
                   self.rect.x * -1 > self.display.get_width(),

                   Any(self.grid[self.y + 1][self.x],
                       self.grid[sub(self.y, 1)][self.x]),

                   self.rect.x % self.display.get_width() != 0):

                diff = self.rect.x % self.display.get_width()
                self.move_all(-diff, 0)
                self.player.move(-diff, 0)
                self.if_in_pivot = True

            elif All(self.player.rect.centerx > self.display.get_rect().centerx, # not in middle of display
                     self.grid[self.y][self.x + 1], # next part of map exists
                     not self.grid[self.y + 1][self.x], # no map above
                     not self.grid[sub(self.y, 1)][self.x]): # no map below

                diff = self.player.rect.centerx - self.display.get_rect().centerx
                self.player.move(-diff, 0)
                self.move_all(-diff, 0)
                self.if_in_pivot = False

        elif mode == BACK:
            if All(not self.if_in_pivot,
                   self.rect.x * -1 > self.display.get_width(),

                   Any(self.grid[self.y + 1][self.x],
                       self.grid[sub(self.y, 1)][self.x]),

                   self.rect.x % self.display.get_width() != 0):

                diff = self.rect.x % self.display.get_width()
                self.move_all(diff, 0)
                self.player.move(diff, 0)

                self.if_in_pivot = True

            elif All(self.player.rect.centerx < self.display.get_rect().centerx,
                     self.rect.x < 0,
                     self.grid[self.y][self.x],
                     not self.grid[self.y + 1][self.x],
                     not self.grid[sub(self.y, 1)][self.x]):

                diff = -self.player.rect.centerx + self.display.get_rect().centerx
                self.player.move(diff, 0)
                self.move_all(diff, 0)
                self.if_in_pivot = False

    def move(self, key_press):
        if self.player.if_climbing:
            if key_press[K_a]:
                self.player.fwd = BACK
            elif key_press[K_d]:
                self.player.fwd = FWD

            if key_press[K_w]:
                self.player.move(0, -5)
                self.camera_check(TOP)

                if self.player.rect.top <= self.current_ladder.top:
                    self.player.rect.bottom = self.current_ladder.top
                    self.player.if_climbing = False

            elif key_press[K_s]:
                self.player.move(0, 5)
                self.camera_check(BOTTOM)

                if self.player.rect.bottom >= self.current_ladder.bottom:
                    self.player.rect.bottom = self.current_ladder.bottom
                    self.player.if_climbing = False
                    self.player.if_falling = True

            elif key_press[K_SPACE]:
                self.player.if_climbing = False
                self.player.if_falling = True
        else:
            if key_press[K_SPACE] and self.player.jump_tick < self.player.max_jump_tick and not self.player.if_falling:
                self.player.move(0, -self.player.jump_steps[self.player.jump_tick])
                self.player.jump_tick += 1

                walls_hit = [w for w in self.walls if self.player.rect.colliderect(w)]

                if walls_hit:
                    self.player.if_falling = True
                    for wall in walls_hit:
                        self.player.move(0, -self.player.rect.top + wall.bottom)

                self.camera_check(TOP)

            else:
                self.player.if_falling = True
                self.player.move(0, 8)
                walls_hit = sum(
                    [[self.walls[i] for i in self.player.rect.collidelistall(self.walls)],
                     [self.ladder_tops[i] for i in self.player.rect.collidelistall(self.ladder_tops)]
                    ],
                    []
                )

                if DEBUG:
                    walls_hit += [self.traps[i] for i in self.player.rect.collidelistall(self.traps)]

                if walls_hit:
                    self.player.if_falling = False
                    self.player.move(0, -self.player.rect.bottom + walls_hit[0].top)
                else:
                    self.player.jump_tick = self.player.max_jump_tick

                if self.player.rect.centery >= self.display.get_height():
                    self.t_coordinates.add(f'grid {self.x}, {self.y}: {self.grid[self.y][self.x]}')

                self.camera_check(BOTTOM)

            move = 5 if self.player.if_moving else 1

            if key_press[K_d]:
                self.player.move(move, 0)
                self.player.if_moving = True
                self.player.fwd       = FWD

                self.camera_check(FWD)

            elif key_press[K_a]:
                self.player.move(-move, 0)
                self.player.if_moving = True
                self.player.fwd       = BACK

                self.camera_check(BACK)

            else:
                self.player.if_moving = False

            if key_press[K_w] and self.player.rect.collidelistall(self.ladders):
                self.current_ladder = self.ladders[self.player.rect.collidelistall(self.ladders)[0]]
                self.player.rect.centerx = self.current_ladder.centerx
                self.player.if_climbing = True
                self.player.if_moving = False
                self.player.if_falling = False

            elif key_press[K_s] and any(self.player.rect.bottom == w.top for w in self.ladder_tops):
                ladder_top = [w for w in self.ladder_tops if self.player.rect.bottom == w.top][0]
                self.player.rect.midtop = ladder_top.midbottom
                self.current_ladder = self.ladders[self.player.rect.collidelistall(self.ladders)[0]]
                self.player.if_climbing = True
                self.player.if_moving = False
                self.player.if_falling = False

            if self.player.if_moving:

                walls_hit = [self.walls[i] for i in self.player.rect.collidelistall(self.walls)]

                for wall in walls_hit:
                    if self.player.fwd == FWD:
                        self.player.move(-self.player.rect.right + wall.left, 0)
                    else:
                        self.player.move(-self.player.rect.left + wall.right, 0)

        if not DEBUG:
            traps_hit = [self.traps[i] for i in self.player.rect.collidelistall(self.traps)]

            if traps_hit:
                self.if_dead = True

        if not self.player.if_falling and not key_press[K_SPACE]:
            self.player.jump_tick = 0

        self.t_grid[self.y][self.x] = self.grid[self.y][self.x]
