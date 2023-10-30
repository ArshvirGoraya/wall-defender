import pygame
from .text import Text
from .button import Button
# from color_schemes import ColorScheme


class StartMenu():
    screen_h: float
    screen_w: float
    # colors: ColorScheme
    TITLE_Y = 0
    CONTROLS_Y = 0

    menu = pygame.sprite.Group()
    button_start_game: pygame.sprite.GroupSingle()

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
                "WALL DEFENDER",
                pygame.Vector2(self.screen_w/2, self.TITLE_Y)
            ),
            Text(
                colors.get_text(),
                40,
                "-=CONTROLS=-",
                pygame.Vector2(self.screen_w/2, self.CONTROLS_Y)
            ),
            Text(
                colors.get_text(),
                40,
                "Move: wasd",
                pygame.Vector2(self.screen_w/2, self.CONTROLS_Y + (40 * 1))
            ),
            Text(
                colors.get_text(),
                40,
                "Attack: arrows or ijkl",
                pygame.Vector2(self.screen_w/2, self.CONTROLS_Y + (40 * 2))
            ),
            Text(
                colors.get_text(),
                40,
                "Run: hold shift",
                pygame.Vector2(self.screen_w/2, self.CONTROLS_Y + (40 * 3))
            ),
            Text(
                colors.get_text(),
                40,
                "Pause: esc",
                pygame.Vector2(self.screen_w/2, self.CONTROLS_Y + (40 * 4))
            ),
            Text(
                colors.get_text(),
                40,
                "Enter wall: enter",
                pygame.Vector2(self.screen_w/2, self.CONTROLS_Y + (40 * 5))
            ),
        )

        self.button_start_game = pygame.sprite.GroupSingle()
        self.button_start_game.add(
            Button(
                colors.get_button_text(),
                colors.get_button_bg(),
                colors.get_button_hover(),
                colors.get_button_pressed(),
                colors.get_button_disabled(),
                False,
                "Start Game",
                40,
                pygame.Vector2(self.screen_w/2, self.screen_h/2)
            )
        )
