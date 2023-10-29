import pygame


class Text(pygame.sprite.Sprite):
    '''Sprite for texts.'''

    def __init__(self, color, font_size, text, pos) -> None:
        super().__init__()
        self.font_size = font_size
        self.text = text

        font = pygame.font.Font('assets/monogram.ttf', int(font_size))

        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=(pos.x, pos.y))
