import pygame


class Player(pygame.sprite.Sprite):
    health: float = 10
    speed = 100

    def __init__(self, color, screen) -> None:
        super().__init__()

        self.color = color
        self.width = 30
        self.height = 30

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((color))

        # Position
        self.x_pos = screen.width/4
        self.y_pos = screen.height/2
        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))

    def update(self, delta) -> None:
        self.destroy_check()
        self.movement(delta)

    def destroy_check(self) -> None:
        if self.health <= 0:
            self.kill()

    def movement(self, delta) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y_pos -= self.speed * delta
        if keys[pygame.K_s]:
            self.y_pos += self.speed * delta
        if keys[pygame.K_d]:
            self.x_pos += self.speed * delta
        if keys[pygame.K_a]:
            self.x_pos -= self.speed * delta

        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))
