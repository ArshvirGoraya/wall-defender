import pygame


class Text(pygame.sprite.Sprite):
    '''Sprite for texts.'''

    def __init__(self, color, font_size, text, pos, centered: bool = True) -> None:
        super().__init__()
        self.font_size = font_size
        self.text = text
        self.color = color

        self.font = pygame.font.Font('assets/monogram.ttf', int(font_size))

        self.image = self.font.render(self.text, True, color)

        if centered:
            self.rect = self.image.get_rect(center=(pos.x, pos.y))
        else:
            self.rect = self.image.get_rect(topleft=(pos.x, pos.y))

        self.centered = centered
        self.pos = pos

    def update_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)

        if self.centered:
            self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        else:
            self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
