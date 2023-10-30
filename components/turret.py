import pygame
from random import randint


class Turret(pygame.sprite.Sprite):

    def __init__(self, wait_time, screen) -> None:
        super().__init__()

        self.y_pos = y_pos
        self.wait_time = wait_time

        self.image = pygame.Surface((2, 2))
        self.image.fill(("WHITE"))
        # self.image.set_alpha(0)
        y_pos = randint(5, screen.width - 5),

        self.rect = self.image.get_rect(center=(screen.x, y_pos))

        self.current_time = wait_time

    def update(self, delta) -> None:
        self.current_time -= delta
        if self.current_time <= self.wait_time:
            self.shoot()
            self.current_time = self.wait_time

    def shoot():
        pass
