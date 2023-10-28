import pygame
from random import randint


class Enemy(pygame.sprite.Sprite):
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, speed, health, color, lefty, screen) -> None:
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
        self.image.blit

        # Assign position: x and y
        self.lefty = lefty  # True = move left. False = move right.

        y = randint(self.top_limit, self.bottom_limit)
        if lefty:  # If lefty, will spawn left and move right.
            x = self.left_limit
        else:
            x = self.right_limit
        self.rect = self.image.get_rect(topleft=(x, y))

        self.x_pos = x  # Required to avoid integer truncating for self.rect.x
        self.y_pos = y

        self.speed = speed
        self.health = health

    def update(self, delta, wall_rect) -> None:
        self.destroy_check(wall_rect)
        self.move(delta)

    def destroy_check(self, wall_rect) -> None:
        if self.health <= 0:
            self.kill()

        # Destroy if collided with wall.
        if self.lefty:
            if self.x_pos+self.WIDTH >= wall_rect.left:
                self.kill()
        else:
            if self.x_pos <= wall_rect.right:
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
