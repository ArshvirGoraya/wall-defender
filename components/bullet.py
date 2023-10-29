import pygame


class Bullet(pygame.sprite.Sprite):
    WIDTH = 10
    HEIGHT = 10
    DAMAGE = 1

    def __init__(self, speed, color, player_pos, direction, enemy_reference, screen) -> None:
        super().__init__()

        self.color = color

        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill((color))

        self.x_pos = player_pos.x
        self.y_pos = player_pos.y
        self.rect = self.image.get_rect(center=(player_pos.x, player_pos.y))

        self.speed = speed
        self.direction = direction
        self.enemy_ref = enemy_reference
        self.screen = screen

    def update(self, delta) -> None:
        self.destroy_check()
        self.collision_check()
        self.movement(delta)

    def movement(self, delta) -> None:
        # FPS-independent movement: at given direction, at a specific speed.
        velocity = self.direction.normalize() * (self.speed * delta)
        self.x_pos += velocity.x
        self.y_pos += velocity.y

        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))

    def collision_check(self) -> None:
        # Destroy enemy and self if collide.
        if pygame.sprite.spritecollide(self, self.enemy_ref, True):
            self.kill()

    def destroy_check(self) -> None:
        # Destroy if goes off screen.
        if (self.x_pos > self.screen.width
            or self.x_pos < 0
            or self.y_pos < 0
                or self.y_pos > self.screen.height):
            self.kill()
