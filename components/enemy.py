import pygame
from random import randint


class Enemy(pygame.sprite.Sprite):
    speed = 50

    health: float = 10
    lefty: bool = True  # If false, will move right.

    WIDTH = 50
    HEIGHT = 50

    # Bounding box:
    right_limit = 0
    left_limit = 0
    top_limit = 0
    bottom_limit = 0

    def __init__(self, color, lefty, screen) -> None:
        super().__init__()  # Get inherited attributes and functions.

        # Defining bounding box to screen.
        self.top_limit = screen.top
        self.left_limit = screen.left

        self.bottom_limit = screen.bottom - self.HEIGHT
        self.right_limit = screen.right - self.WIDTH

        # Assign color to sprite:
        self.color = color
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill((color))
        self.lefty = lefty

        # Assign position: x and y
        y = randint(self.top_limit, self.bottom_limit)
        if lefty:  # If lefty, will spawn left and move right.
            x = self.left_limit
        else:
            x = self.right_limit
        self.rect = self.image.get_rect(topleft=(x, y))

        self.x_pos = x  # Required to avoid integer truncating for self.rect.x
        self.y_pos = y

    def update(self, delta: float) -> None:
        self.destroy_check()
        self.move(delta)

    def destroy_check(self) -> None:
        if self.health <= 0:
            self.kill()

    # Movement (frame-rate independent)
    def move(self, delta: float) -> None:
        if self.lefty:
            self.x_pos += self.speed * delta
        else:
            self.x_pos -= self.speed * delta

        self.rect.x = self.x_pos  # Avoid integer truncating
        self.rect.y = self.y_pos

        # Collision checks:
