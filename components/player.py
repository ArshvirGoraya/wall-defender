import pygame


class Player(pygame.sprite.Sprite):
    health: float = 10
    speed = 250
    velocity = pygame.Vector2(0, 0)
    max_velocity = 200

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
        # Get direction:
        direction = pygame.Vector2(0, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction.y += -1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_a]:
            direction.x += -1

        if direction.length() > 0:
            # Normalzied movement: diagonal is not faster.
            # Delta: frame-rate independent.
            velocity = direction.normalize() * (self.speed * delta)
            self.x_pos += velocity.x
            self.y_pos += velocity.y

        # if direction.length() == 0:
        #     pass

        # Set new position:
        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))
