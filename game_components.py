import pygame

from random import randint

from components.wall import Wall
from components.enemy import Enemy
from components.ammo import Ammo
from components.player import Player
from components.bullet import Bullet
from components.turret import Turret

from color_schemes import ColorScheme


class GameComponents():
    # colors: ColorScheme  # Holds colors for different components.
    # screen: pygame.surface.Surface  # Info for where to draw components.
    INITIAL_SPAWN_AMMO_MIN = 1
    INITIAL_SPAWN_AMMO_MAX = 10

    INITIAL_BULLET_SPEED = 400

    AMMO_SECONDS = 5

    # spawn_ammo_min = INITIAL_SPAWN_AMMO_MIN
    # spawn_ammo_max = INITIAL_SPAWN_AMMO_MAX

    bullet_speed = INITIAL_BULLET_SPEED

    def __init__(self, colors: ColorScheme, screen: pygame.surface.Surface):
        self.colors = colors
        self.screen = screen

        # Groups: ###############################
        self.wall = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        self.ammo = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.bullet = pygame.sprite.Group()
        self.turret = pygame.sprite.Group()

        # WALL ###############################
        self.create_wall()
        # PLAYER ###############################
        self.create_player()

    def create_player(self):
        self.player.add(
            Player(
                color=self.colors.get_player(),
                screen=self.screen.get_rect(),
                wall_reference=self.wall,
                ammo_reference=self.ammo,
                enemy_reference=self.enemy
            )
        )

    def get_player(self) -> pygame.sprite.Sprite():
        return self.player.sprite

    def create_wall(self):
        self.wall.add(
            Wall(
                color=self.colors.get_wall(),
                screen=self.screen.get_rect(),
                enemy_reference=self.enemy
            )
        )

    def get_wall(self) -> pygame.sprite.Sprite():
        return self.wall.sprite

    # ENEMY ###############################

    def spawn_enemy(self, current_wave) -> None:
        self.enemy.add(
            Enemy(
                health=10,
                color=self.colors.get_enemy(),
                lefty=randint(0, 1),
                screen=self.screen.get_rect(),
                ammo_reference=self.ammo,
                current_wave=current_wave
            )
        )
    # AMMO ###############################

    def spawn_ammo(self) -> None:
        self.ammo.add(
            Ammo(
                self.colors.get_ammo(),
                self.screen.get_rect(),
                # send rect if wall sprite exist or none
                self.wall.sprite.rect if self.wall.sprite != None else None,
                randint(self.AMMO_SECONDS, self.AMMO_SECONDS+5),  # seconds
            )
        )

    # BULLET ###############################
    def spawn_bullet(self, bullet_direction: pygame.Vector2, position: pygame.Vector2) -> None:
        self.bullet.add(
            Bullet(
                speed=self.bullet_speed,
                color=self.colors.get_player(),
                player_pos=position,
                direction=bullet_direction,
                enemy_reference=self.enemy,
                screen=self.screen.get_rect()
            )
        )

    def spawn_turret(self, screen_width, screen_height):
        self.turret.add(
            Turret(
                5,  # wait time
                screen_width,
                screen_height,
                self,
            )
        )

    def reset_to_initial(self):
        self.spawn_ammo_min = self.INITIAL_SPAWN_AMMO_MIN
        self.spawn_ammo_max = self.INITIAL_SPAWN_AMMO_MAX

        self.bullet_speed = self.INITIAL_BULLET_SPEED
