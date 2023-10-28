import pygame


class Wall(pygame.sprite.Sprite):
    health: float = 10

    def __init__(self, color, screen) -> None:
        super().__init__()  # Get inherited attributes and functions.

        self.color = color
        self.width = 100
        # Height = height of screen.
        self.height = screen.height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((color))

        # Position = middle of screen (horizontal).
        self.rect = self.image.get_rect(topright=(screen.width / 2, 0))

    def update(self) -> None:
        self.destroy_check()

    def destroy_check(self) -> None:
        if self.health <= 0:
            self.kill()
