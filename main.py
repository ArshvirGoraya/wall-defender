import pygame
import random
import array as arr  # Incase: don't want to use lists.
import time

from color_schemes import ColorScheme
from components.wall import Wall
from components.enemy import Enemy
from components.ammo import Ammo

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
WALL_POSITION = pygame.Vector2(screen_w/2, 0)

wall = pygame.sprite.GroupSingle()
wall.add(
    Wall(
        color=colors.get_wall(),
        screen=screen.get_rect()
    )
)


# ENEMY ###############################
enemy = pygame.sprite.Group()
enemy.add(
    Enemy(
        speed=300,
        health=10,
        color=colors.get_enemy(),
        lefty=False,
        screen=screen.get_rect()
    )
)
enemy.add(
    Enemy(
        speed=300,
        health=10,
        color=colors.get_enemy(),
        lefty=True,
        screen=screen.get_rect()
    )
)
# AMMO ###############################
ammo = pygame.sprite.Group()


def spawn_ammo() -> None:
    ammo.add(
        Ammo(
            colors.get_ammo(),
            screen.get_rect(),
            wall.sprite.rect
        )
    )


event_ammo_spawn = pygame.USEREVENT + 1
ammo_timer = pygame.time.set_timer(event_ammo_spawn, 1000)

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

        if event.type == event_ammo_spawn:
            spawn_ammo()

    screen.fill((colors.get_ground()))
    wall.draw(screen)
    enemy.draw(screen)
    enemy.update(delta, wall.sprite.rect)

    ammo.draw(screen)
    ammo.update(delta)

    pygame.display.update()
    clock.tick(60)  # FPS limited
