import pygame
import random
import array as arr  # Don't want to use lists.
from color_schemes import ColorScheme

pygame.init()

# Window Info ###############################
pygame.display.set_caption("Resource Defender")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

# Screen Display ###########################
screen_w = 1920 / 2
screen_h = 1080 / 2
screen = pygame.display.set_mode((screen_w, screen_h))
# screen = pygame.display.set_mode((1920/2, 1080/2), pygame.RESIZABLE)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Colors
colors = ColorScheme(ColorScheme.S_BLUEBERRY)
screen.fill((colors.get_ground()))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  # Exits while loop immediately.

    pygame.display.flip()
