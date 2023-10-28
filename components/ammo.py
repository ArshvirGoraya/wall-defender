import pygame
from random import randint


class Ammo(pygame.sprite.Sprite):
    rotation = 0
    rotation_speed: float = 100

    def __init__(self, color, screen, wall, secs) -> None:
        super().__init__()  # Get inherited attributes and functions.

        self.width = 25
        self.height = 25

        # Define borders: where ammo can spawn.
        # Right and left of the wall: Not on the wall.
        # Also: has some padding around the screen/wall.

        # Spawn at random position within the given border:
        if wall:
            self.lefty = randint(0, 1)
            if self.lefty:
                self.ammo_border = pygame.Rect(
                    screen.left + self.width,
                    screen.top + self.height,
                    wall.left - self.width,
                    screen.height - self.height
                )
            else:
                self.ammo_border = pygame.Rect(
                    wall.right + self.width,
                    screen.top + self.height,
                    screen.right - wall.right - self.width,
                    screen.height - self.height
                )
        else:
            self.ammo_border = pygame.Rect(
                screen.left + self.width,
                screen.top + self.height,
                screen.right - self.width,
                screen.height - self.height
            )

        self.color = color

        self.image = pygame.Surface(
            # conversion needed for rotation.
            (self.width, self.height)).convert_alpha()

        self.image.fill((self.color))
        self.o_image = self.image.copy()  # Keep reference to original image.

        self.x = randint(self.ammo_border.left,
                         self.ammo_border.right)
        self.y = randint(self.ammo_border.top,
                         self.ammo_border.bottom)

        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Timer until despawn
        self.start_time = pygame.time.get_ticks()
        self.end_time = self.start_time + secs

    def update(self, delta) -> None:
        # self.rotate(delta)
        self.start_time += delta
        self.destroy_check()

    def rotate(self, delta) -> None:
        self.rotation += self.rotation_speed * delta
        self.image = pygame.transform.rotate(self.o_image, self.rotation)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def destroy_check(self) -> None:
        # pygame.sprite.spritecollide(self, )

        if self.start_time >= self.end_time:
            self.kill()
