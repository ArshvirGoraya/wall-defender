import pygame
import random
import array as arr  # Incase: don't want to use lists.
import time

from color_schemes import ColorScheme
from components.wall import Wall
from components.enemy import Enemy

pygame.init()

# Window Info ###############################
pygame.display.set_caption("Resource Defender")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

# Screen Display ###########################
screen_w = 1920 * 0.8
screen_h = 1080 * 0.8
# screen = pygame.display.set_mode((screen_w, screen_h))
screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Colors
colors = ColorScheme(ColorScheme.S_DARK)
# colors.randomize()


# WALL ###############################
wall = pygame.sprite.GroupSingle()
wall.add(
    Wall(
        width=100,
        height=screen_h,
        color=colors.get_wall(),
        x=screen_w/2,   # top right
        y=0             # top right
    )
)
# ENEMY ###############################
enemy = pygame.sprite.Group()
enemy.add(
    Enemy(
        color=colors.get_enemy(),
        lefty=False,
        screen=screen.get_rect()
    )
)

# Enum: Game States
GAME = 0
PAUSE = 1
FAIL = 2
UPGRADE = 3

game_state = GAME


clock = pygame.time.Clock()  # To limit frame rate.
previous_time = time.time()  # For delta time (frame-rate independent).

while True:
    delta = time.time() - previous_time
    previous_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  # Exits while loop immediately.

    screen.fill((colors.get_ground()))
    wall.draw(screen)
    enemy.draw(screen)
    enemy.update(delta=delta)

    pygame.display.update()
    # clock.tick(240)  # FPS limited
