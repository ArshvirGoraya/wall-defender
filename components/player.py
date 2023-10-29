import pygame


class Player(pygame.sprite.Sprite):
    health: float = 10
    speed = 250
    running = False
    ammo_count: int = 100000

    # Shoot wait time:
    shoot_wait_millis = 0.5
    shoot_wait_current = 0

    velocity = pygame.Vector2(0, 0)

    def __init__(self, color, screen, ammo_reference, enemy_reference) -> None:
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

        self.ammo_ref = ammo_reference
        self.enemy_ref = enemy_reference

    def update(self, delta) -> None:
        self.destroy_check()
        self.collision_check()
        self.movement(delta)

        if self.shoot_wait_current > 0:
            self.shoot_wait_current -= delta

    def can_shoot(self) -> bool:
        return self.shoot_wait_current <= 0

    # Called from event loop directly.
    def shooting(self) -> pygame.Vector2:
        direction = pygame.Vector2(0, 0)
        if not self.can_shoot():
            return direction

        keys = pygame.key.get_pressed()

        if keys[pygame.K_i] or keys[pygame.K_UP]:
            direction.y += -1
        if keys[pygame.K_k] or keys[pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_l] or keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[pygame.K_j] or keys[pygame.K_LEFT]:
            direction.x += -1

        if direction.length() != 0:
            self.triggered_shot()

        # MAY NEED TO BE A COPY (does refernce die when this object does?)
        return direction

    def triggered_shot(self) -> None:
        self.ammo_count -= 1
        self.shoot_wait_current = self.shoot_wait_millis

    def collision_check(self) -> None:
        # Increase ammo by the amount we collided with.
        self.ammo_count += pygame.sprite.spritecollide(
            self, self.ammo_ref, True).__len__()

        for enemy in pygame.sprite.spritecollide(self, self.enemy_ref, True):
            self.health -= enemy.get_damage()
            # print("Player Health: ", self.health)

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

        self.running = keys[pygame.K_LSHIFT]

        # Get Velocity
        if direction.length() > 0:
            # Normalzied movement: diagonal is not faster.
            # Delta: frame-rate independent.
            # velocity = direction.normalize() * ((self.speed) * delta) # no specials
            speed = self.speed
            if self.running:
                speed *= 2

            self.velocity = direction.normalize() * (speed * delta)
            self.x_pos += self.velocity.x
            self.y_pos += self.velocity.y

        # Set new position:
        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))
