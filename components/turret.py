import pygame
from random import randint


class Turret(pygame.sprite.Sprite):

    def __init__(self, color, wait_time, screen_width, screen_height, game_components_reference) -> None:
        super().__init__()

        self.wait_time = wait_time

        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.image.set_alpha(50)

        # print("screen height: ", int(screen_height))

        self.y_pos = randint(5, int(screen_height))
        self.x_pos = screen_width / 2

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        self.current_time = wait_time

        self.game_components = game_components_reference

    def update(self, delta) -> None:
        self.current_time -= delta
        if self.current_time <= 0:
            self.shoot()
            self.current_time = self.wait_time

    def shoot(self):
        # print("SHOOT!")
        self.game_components.spawn_bullet(
            pygame.Vector2(-1, 0),
            pygame.Vector2(self.x_pos, self.y_pos),
        )
        self.game_components.spawn_bullet(
            pygame.Vector2(1, 0),
            pygame.Vector2(self.x_pos, self.y_pos),
        )
