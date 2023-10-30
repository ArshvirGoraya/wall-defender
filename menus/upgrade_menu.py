import pygame
from .text import Text
from .button import Button
# from color_schemes import ColorScheme


class UpgradeMenu():
    screen_h: float
    screen_w: float
    # colors: ColorScheme
    TITLE_Y = 0
    CONTROLS_Y = 0

    menu = pygame.sprite.Group()
    button: pygame.sprite.GroupSingle()

    def __init__(self, screen, colors):
        self.screen_h = screen.get_rect().height
        self.screen_w = screen.get_rect().width
        self.colors = colors

        self.TITLE_Y = self.screen_h * 0.2
        self.CONTROLS_Y = self.screen_h * 0.7

        self.menu.add(
            Text(
                colors.get_text(),
                80,
                "UPGRADE",
                pygame.Vector2(self.screen_w/2, self.TITLE_Y)
            ),
        )
        # Speed
        self.speed_up = pygame.sprite.GroupSingle()
        self.speed_bullet = pygame.sprite.GroupSingle()
        self.speed_shoot = pygame.sprite.GroupSingle()
        # Ammo
        self.ammo_cap = pygame.sprite.GroupSingle()
        self.ammo_spawn_rate = pygame.sprite.GroupSingle()
        # Health
        self.health_player = pygame.sprite.GroupSingle()
        self.health_wall = pygame.sprite.GroupSingle()
        # Turret 0_0
        # self.turret = pygame.sprite.GroupSingle()

        self.buttons = {
            self.health_player: "Player Health + 1",
            self.health_wall: "Wall Health + 1",
            self.ammo_cap: "Ammo Cap + 1",
            self.ammo_spawn_rate: "Ammo Spawn + 1",
            self.speed_up: "Speed + 1",
            self.speed_shoot: "Shoot Speed + 1",
            self.speed_bullet: "Bullet Speed + 1",
            # self.turret: "Turret + 1",
        }
        button_count = 0
        for button in self.buttons:
            button.add(
                self.create_button(
                    self.buttons[button],
                    pygame.Vector2(self.screen_w/2,
                                   self.screen_h * 0.4 + (50 * button_count))
                )
            )
            button_count += 1

    def create_button(self, text, pos):
        return Button(
            self.colors.get_button_text(),
            self.colors.get_button_bg(),
            self.colors.get_button_hover(),
            self.colors.get_button_pressed(),
            self.colors.get_button_disabled(),
            False,
            text,
            40,
            pos
        )
