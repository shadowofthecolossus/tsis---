import pygame

# simple text drawing tool
def draw_text(screen, text, x, y, font, color=(255, 255, 255), center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)