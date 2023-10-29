import pygame
import random
# import array as arr  # Incase: don't want to use lists.
import time

from color_schemes import ColorScheme
from components.wall import Wall
from components.enemy import Enemy
from components.ammo import Ammo
from components.player import Player
from components.bullet import Bullet
from game_components import GameComponents

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
colors.randomize()

# Player, Ammo, Wall, Enemies, Bullets, etc.
game_components = GameComponents(colors, screen)


# Inital ammo
for x in range(random.randint(5, 10)):
    game_components.spawn_ammo()

# CUSTOM EVENTS & TIMERS ###############################
event_ammo_spawn = pygame.USEREVENT + 1
event_enemy_spawn = pygame.USEREVENT + 2

ammo_timer = pygame.time.set_timer(event_ammo_spawn, 1000)
enemy_timer = pygame.time.set_timer(event_enemy_spawn, 1000)


# Enum: Game States (don't want/need enum import)
GAME = 0
START = 1
PAUSE = 2
FAIL = 3
UPGRADE = 4

game_state = START

clock = pygame.time.Clock()  # To limit frame rate.
previous_time = time.time()  # For delta time (frame-rate independent).

while True:
    delta = time.time() - previous_time
    previous_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  # Exits while loop immediately.

        if game_state == GAME:
            # Match case is kind of annoying in python: can't just match with event_ammo_spawn
            if event.type == event_ammo_spawn:
                game_components. spawn_ammo()

            elif event.type == event_enemy_spawn:
                game_components.spawn_enemy()

    if game_state == START:
        screen.fill("WHITE")

        #
        #
        #
        #

    elif game_state == GAME:
        screen.fill((colors.get_ground()))

        game_components.wall.update()
        game_components.wall.draw(screen)

        game_components.enemy.update(delta)
        game_components.enemy.draw(screen)

        # Ammo resources on the ground.
        game_components.ammo.update(delta)
        game_components.ammo.draw(screen)

        game_components.player.update(delta)
        game_components.player.draw(screen)

        # Update all spawned bullets:
        game_components.bullet.update(delta)
        game_components.bullet.draw(screen)

        # Spawn bullet if player has shot:
        # If player has ammo,
        # check if is shooting and get direction of shot.
        if game_components.player.sprite.ammo_count:
            bullet_direction = game_components.player.sprite.shooting()
            if bullet_direction.length() != 0:
                game_components.spawn_bullet(bullet_direction)

    pygame.display.update()
    clock.tick(60)  # FPS limited
