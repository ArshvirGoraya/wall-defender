import pygame


class Player(pygame.sprite.Sprite):
    INITIAL_HEALTH = 10
    INITIAL_MAX_HEALTH = 10

    INITIAL_AMMO = 10
    INITIAL_MAX_AMMO = 50

    INITIAL_SPEED = 150

    INITIAL_SHOOT_WAIT_TIME = 0.5

    health: float = INITIAL_HEALTH
    max_health: float = INITIAL_MAX_HEALTH

    ammo_count: int = INITIAL_AMMO
    max_ammo: int = INITIAL_MAX_AMMO

    speed = INITIAL_SPEED

    # Shoot wait time:
    shoot_wait_millis = INITIAL_SHOOT_WAIT_TIME
    shoot_wait_current = 0

    running = False
    velocity = pygame.Vector2(0, 0)

    # STATES
    IN_WALL = 0
    NEAR_WALL = 1
    OUT_WALL = 2
    move_state = OUT_WALL

    WIDTH = 30
    HEIGHT = 30

    def __init__(self, color, screen, wall_reference, ammo_reference, enemy_reference) -> None:
        super().__init__()

        self.color = color
        self.width = self.WIDTH
        self.height = self.HEIGHT

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((color))

        # Position
        self.x_pos = screen.width/4
        self.y_pos = screen.height/2
        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))

        self.ammo_ref = ammo_reference
        self.enemy_ref = enemy_reference
        self.wall_ref = wall_reference
        self.screen = screen

    def update(self, delta) -> None:
        self.destroy_check()
        self.wall_check()
        self.collision_check()
        self.movement(delta)

        if self.shoot_wait_current > 0:
            self.shoot_wait_current -= delta

    def wall_check(self):
        if self.wall_ref.sprite == None:
            return
        if self.move_state == self.IN_WALL:
            return

        # Wall left and right:
        if (self.x_pos >= self.wall_ref.sprite.rect.left and self.x_pos <= self.wall_ref.sprite.rect.right):
            self.move_state = self.NEAR_WALL
        else:
            self.move_state = self.OUT_WALL

    def enter_wall(self):
        self.move_state = self.IN_WALL
        # Set to width of wall.
        self.width = self.wall_ref.sprite.rect.width

        # Set x to middle of wall.
        self.x_pos = self.wall_ref.sprite.rect.x + self.wall_ref.sprite.rect.width / 2

        # asd

    def exit_wall(self):
        self.move_state = self.NEAR_WALL
        #
        self.width = self.WIDTH

    def can_shoot(self) -> bool:
        return self.shoot_wait_current <= 0

    # Called from event loop directly.
    def shooting(self) -> pygame.Vector2:
        direction = pygame.Vector2(0, 0)
        if not self.can_shoot():
            return direction

        keys = pygame.key.get_pressed()

        # Cant shoot vertically when in wall
        if self.move_state != self.IN_WALL:
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
        # For each 1 ammo, should get 5.
        self.ammo_count += pygame.sprite.spritecollide(
            self, self.ammo_ref, True).__len__() * 5

        # Cant take damage while in wall mode:
        if self.move_state != self.IN_WALL:
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

        # Cant move horizontally when in wall.
        if self.move_state != self.IN_WALL:
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
            # Move faster when in wall:
            if self.move_state == self.IN_WALL:
                speed *= 2
            if self.running:
                speed *= 2

            self.velocity = direction.normalize() * (speed * delta)
            self.x_pos += self.velocity.x
            self.y_pos += self.velocity.y

            # X limits
            self.x_pos = pygame.math.clamp(
                self.x_pos,
                0,
                self.screen.width,
            )
            # Y limits
            self.y_pos = pygame.math.clamp(
                self.y_pos,
                0 + self.height / 2,
                self.screen.height - self.height / 2,
            )

        # Set new position: (drawn here)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((self.color))

        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))

    def reset_to_initial(self):
        self.health = self.INITIAL_HEALTH
        self.max_health = self.INITIAL_MAX_HEALTH
        self.ammo_count = self.INITIAL_AMMO
        self.max_ammo = self.INITIAL_MAX_AMMO
        self.speed = self.INITIAL_SPEED
        self.shoot_wait_millis = self.INITIAL_SHOOT_WAIT_TIME

        self.move_state = self.OUT_WALL

        self.x_pos = self.screen.width/4
        self.y_pos = self.screen.height/2
        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))

        self.width = self.WIDTH

    def set_variables(self, variables: dict):
        self.health = variables["health"]
        self.max_health = variables["max_health"]
        self.ammo_count = variables["ammo_count"]
        self.max_ammo = variables["max_ammo"]
        self.speed = variables["speed"]
        self.shoot_wait_millis = variables["shoot_wait_millis"]

        self.move_state = variables["move_state"]
        self.rect = variables["rect"]
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y

        self.width = self.rect.width

        # X's position should be in the middle of wall.
        if self.move_state == self.IN_WALL:
            self.x_pos = self.wall_ref.sprite.rect.x + self.wall_ref.sprite.rect.width / 2

    def is_near_wall(self) -> bool:
        return self.move_state == self.NEAR_WALL
