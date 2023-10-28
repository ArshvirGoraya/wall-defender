import pygame
from random import randint


class Ammo(pygame.sprite.Sprite):
    rotation = 0
    rotation_speed: float = 100

    def __init__(self, color, screen, wall) -> None:
        super().__init__()  # Get inherited attributes and functions.

        self.width = 25
        self.height = 25

        # Define borders: where ammo can spawn.
        # Right and left of the wall: Not on the wall.
        # Also: has some padding around the screen/wall.

        self.ammo_border_left = pygame.Rect(
            screen.left + self.width,
            screen.top + self.height,
            wall.left - self.width,
            screen.height - self.height
        )

        self.ammo_border_right = pygame.Rect(
            wall.right + self.width,
            screen.top + self.height,
            screen.right - wall.right - self.width,
            screen.height - self.height
        )

        self.color = color

        self.image = pygame.Surface(
            # conversion needed for rotation.
            (self.width, self.height)).convert_alpha()

        self.image.fill((self.color))
        self.o_image = self.image.copy()  # Keep reference to original image.

        # Spawn at random position within the given border:
        self.lefty = randint(0, 1)

        if self.lefty:

            self.x = randint(self.ammo_border_left.left,
                             self.ammo_border_left.right)
            self.y = randint(self.ammo_border_left.top,
                             self.ammo_border_left.bottom)

        else:
            self.x = randint(self.ammo_border_right.left,
                             self.ammo_border_right.right)
            self.y = randint(self.ammo_border_right.top,
                             self.ammo_border_right.bottom)

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, delta) -> None:
        self.rot(delta)

        # self.destroy_check()

    def rot(self, delta) -> None:
        self.rotation += self.rotation_speed * delta
        self.image = pygame.transform.rotate(self.o_image, self.rotation)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    # def destroy_check(self) -> None:
    #     pass
