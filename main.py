import pygame
import random
import array as arr  # Incase: don't want to use lists.
import time

from color_schemes import ColorScheme
from components.wall import Wall
from components.enemy import Enemy
from components.ammo import Ammo
from components.player import Player

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

# Groups: ###############################
wall = pygame.sprite.GroupSingle()
enemy = pygame.sprite.Group()
ammo = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()

# WALL ###############################
wall.add(
    Wall(
        color=colors.get_wall(),
        screen=screen.get_rect(),
        enemy_reference=enemy
    )
)
# ENEMY ###############################


def spawn_enemy() -> None:
    enemy.add(
        Enemy(
            speed=300,
            health=10,
            color=colors.get_enemy(),
            lefty=random.randint(0, 1),
            screen=screen.get_rect(),
            ammo_reference=ammo
        )
    )
# AMMO ###############################


def spawn_ammo() -> None:
    ammo.add(
        Ammo(
            colors.get_ammo(),
            screen.get_rect(),
            # send rect if wall sprite exist or none
            wall.sprite.rect if wall.sprite != None else None,
            random.randint(1, 10),  # seconds
        )
    )


# Inital ammo
for x in range(random.randint(5, 10)):
    spawn_ammo()

# PLAYER ###############################
player.add(
    Player(
        color=colors.get_player(),
        screen=screen.get_rect(),
        ammo_reference=ammo,
        enemy_reference=enemy
    )
)

# Timers ###############################
event_ammo_spawn = pygame.USEREVENT + 1
ammo_timer = pygame.time.set_timer(event_ammo_spawn, 1000)

event_enemy_spawn = pygame.USEREVENT + 2
enemy_timer = pygame.time.set_timer(event_enemy_spawn, 1000)


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
        # match event.type:
        #     case pygame.QUIT:
        #         pygame.quit()
        #         quit()  # Exits while loop immediately.

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  # Exits while loop immediately.

        elif event.type == event_ammo_spawn:
            spawn_ammo()

        elif event.type == event_enemy_spawn:
            spawn_enemy()

    screen.fill((colors.get_ground()))

    wall.update()
    wall.draw(screen)

    enemy.update(delta)
    enemy.draw(screen)

    ammo.update(delta)
    ammo.draw(screen)

    player.update(delta)
    player.draw(screen)

    pygame.display.update()
    clock.tick(60)  # FPS limited
