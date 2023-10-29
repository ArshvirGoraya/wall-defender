import pygame
from .text import Text
from .button import Button
# from color_schemes import ColorScheme


class WinMenu():
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
                "YOU WIN!",
                pygame.Vector2(self.screen_w/2, self.TITLE_Y)
            ),
            # Text(
            #     colors.get_text(),
            #     40,
            #     "-=CONTROLS=-",
            #     pygame.Vector2(self.screen_w/2, self.CONTROLS_Y)
            # )
        )

        self.button = pygame.sprite.GroupSingle()
        self.button.add(
            Button(
                colors.get_button_text(),
                colors.get_button_bg(),
                colors.get_button_hover(),
                colors.get_button_pressed(),
                colors.get_button_disabled(),
                False,
                "Endless Mode: Keep Going",
                40,
                pygame.Vector2(self.screen_w/2, self.screen_h/2)
            )
        )
