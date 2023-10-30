import pygame
from random import randint


class Enemy(pygame.sprite.Sprite):
    WIDTH = 50
    HEIGHT = 50
    DAMAGE = 1

    ENEMY_SPACING = 1920 * 2

    SPEED = 300

    def __init__(self, health, color, lefty, screen, ammo_reference, current_wave) -> None:
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
            x = self.left_limit - \
                randint(0, (self.ENEMY_SPACING + current_wave*4))
        else:
            x = self.right_limit + \
                randint(0, (self.ENEMY_SPACING + current_wave*4))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.x_pos = x  # Required to avoid integer truncating for self.rect.x
        self.y_pos = y

        self.speed = self.SPEED + (current_wave * 2)
        self.health = health

        self.ammo_ref = ammo_reference

    def update(self, delta) -> None:
        self.destroy_check()
        self.collision_check()
        self.move(delta)

    def collision_check(self) -> None:
        pygame.sprite.spritecollide(self, self.ammo_ref, True)

    def destroy_check(self) -> None:
        if self.health <= 0:
            self.kill()

    # Movement (frame-rate independent)
    def move(self, delta: float) -> None:
        if self.lefty:
            self.x_pos += self.speed * delta
        else:
            self.x_pos -= self.speed * delta

        # Avoids integer truncating (framerate independence)
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def get_damage(self):
        return self.DAMAGE
