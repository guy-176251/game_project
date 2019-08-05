import pygame

size = (400,400)
display = pygame.display.set_mode(size)
bg = pygame.Surface(size)
bg.fill((255,255,255))

def refresh(rects = None):
    display.blit(bg, (0,0))
    if rects:
        for r in rects:
            display.blit(pygame.Surface(r.size), r)
        intersects = [ [ r1.clip(rects[i]) for i in r1.collidelistall(rects) if rects[i] is not r1 ]for r1 in rects ]
        for l in intersects:
            for r in l:
                surf = pygame.Surface(r.size)
                surf.fill((255,0,0))
                display.blit(surf, r)

    pygame.display.flip()
