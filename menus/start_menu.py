import pygame
from text import Text  # Extends Sprite
from button import Button  # Extends Sprite


class StartMenu(pygame.sprite.Group()):
    '''
    Group: can hold many sprites.
    This group is intended to only hold text and buttons.
    '''
    TITLE_SIZE: int = 80

    def __init__(self, colors, screen) -> None:
        super().__init__()
        self.screen = screen

        TITLE_Y = screen.height * 0.2
        CONTROLS_Y = screen.height * 0.7

        self.add(
            Text(
                colors.get_text(),
                self.TITLE_SIZE,
                "WALL DEFENDER",
                pygame.Vector2(screen.width/2, TITLE_Y)
            ),
        )

    def add_text(self, text: Text):
        self.add(
            text
        )

    def add_button(self, button: Button):
        self.add(
            button
        )
