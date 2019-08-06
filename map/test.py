import pygame

size = (400,400)
display = pygame.display.set_mode(size)
bg = pygame.Surface(size)
bg.fill((255,255,255))

def refresh(rects = None):
    display.blit(bg, (0,0))
    if rects:

        display.blits([ (pygame.Surface(r.size), r) for r in rects])
        intersects = sum( [ [ r1.clip(rects[i]) for i in r1.collidelistall(rects) if rects[i] is not r1 ]
                          for r1 in rects ],
                         [])

        print(intersects)

        dupes = []
        for r in intersects:
            if (r.topleft, r.size) not in dupes:
                surf = pygame.Surface(r.size)
                surf.fill((255,0,0))
                display.blit(surf, r)
                dupes.append((r.topleft, r.size))

    pygame.display.flip()
