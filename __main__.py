import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.run_imgs = [pygame.image.load(n)
                         for n in ('running/2.png',
                                   'running/3.png',
                                   'running/4.png')]

        self.run_ind = 0
        self.run_fwd = True

        self.image = self.run_imgs[self.run_ind]
        self.rect  = self.image.get_rect()
        self.rect.y = 425

    def run_animation(self):

        if self.run_fwd:
            self.run_ind += 1
        else:
            self.run_ind -= 1

        if self.run_ind == 2 and self.run_fwd:
            self.run_fwd = False
        elif self.run_ind == 0 and not self.run_fwd:
            self.run_fwd = True

        self.image = self.run_imgs[self.run_ind]

    def update(self, key_press):
        #if key_press[K_w]:
        #    self.rect.move_ip(0, -1)
        #if key_press[K_s]:
        #    self.rect.move_ip(0, 1)
        if key_press[K_a]:
            self.rect.move_ip(-1, 0)
        if key_press[K_d]:
            self.rect.move_ip(1, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    bg     = pygame.image.load('bg.jpg').convert()

    my_sprite = Player()
    my_group  = pygame.sprite.Group(my_sprite)

    ANIM_TICK = pygame.USEREVENT + 1
    pygame.time.set_timer(ANIM_TICK, 100)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            elif event.type == QUIT:
                return
            elif event.type == ANIM_TICK:
                my_sprite.run_animation()

        screen.blit(bg, (0,0))
        my_sprite.update(pygame.key.get_pressed())

        for thing in my_group:
            screen.blit(thing.image, thing.rect)

        pygame.display.flip()

main()
