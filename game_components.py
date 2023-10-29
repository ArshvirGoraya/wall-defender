import pygame

from random import randint

from components.wall import Wall
from components.enemy import Enemy
from components.ammo import Ammo
from components.player import Player
from components.bullet import Bullet

from color_schemes import ColorScheme


class GameComponents():
    # colors: ColorScheme  # Holds colors for different components.
    # screen: pygame.surface.Surface  # Info for where to draw components.

    def __init__(self, colors: ColorScheme, screen: pygame.surface.Surface):
        self.colors = colors
        self.screen = screen

        # Groups: ###############################
        self.wall = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        self.ammo = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.bullet = pygame.sprite.Group()

        # WALL ###############################
        self.wall.add(
            Wall(
                color=self.colors.get_wall(),
                screen=self.screen.get_rect(),
                enemy_reference=self.enemy
            )
        )
        # PLAYER ###############################
        self.player.add(
            Player(
                color=self.colors.get_player(),
                screen=self.screen.get_rect(),
                ammo_reference=self.ammo,
                enemy_reference=self.enemy
            )
        )

    def get_player(self) -> pygame.sprite.Sprite():
        return self.player.sprite

    # ENEMY ###############################

    def spawn_enemy(self) -> None:
        self.enemy.add(
            Enemy(
                speed=300,
                health=10,
                color=self.colors.get_enemy(),
                lefty=randint(0, 1),
                screen=self.screen.get_rect(),
                ammo_reference=self.ammo
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
                randint(1, 10),  # seconds
            )
        )

    # BULLET ###############################
    def spawn_bullet(self, bullet_direction: pygame.Vector2) -> None:
        self.bullet.add(
            Bullet(
                speed=400,
                color=self.colors.get_player(),
                player_pos=pygame.Vector2(
                    self.player.sprite.x_pos, self.player.sprite.y_pos),
                direction=bullet_direction,
                enemy_reference=self.enemy,
                screen=self.screen.get_rect()
            )
        )
