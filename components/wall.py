import pygame


class Wall(pygame.sprite.Sprite):
    health: float = 10

    def __init__(self, width, height, color, x, y) -> None:
        super().__init__()  # Get inherited attributes and functions.

        self.width = width
        self.height = height
        self.color = color

        # Sprite requires these 2 vars at least:
        self.image = pygame.Surface((width, height))
        self.image.fill((color))
        self.rect = self.image.get_rect(topright=(x, y))

    def update(self) -> None:
        self.destroy_check()

    def destroy_check(self) -> None:
        if self.health <= 0:
            self.kill()
