import pygame


class Wall(pygame.sprite.Sprite):
    INITIAL_HEALTH = 10000
    INITIAL_MAX_HEALTH = 10

    health: float = INITIAL_HEALTH
    max_health: float = INITIAL_MAX_HEALTH

    def __init__(self, color, screen, enemy_reference) -> None:
        super().__init__()  # Get inherited attributes and functions.

        self.color = color
        self.width = 100
        # Height = height of screen.
        self.height = screen.height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((self.color))

        # Position = middle of screen (horizontal).
        self.rect = self.image.get_rect(midtop=(screen.width / 2, 0))

        self.enemy_ref = enemy_reference
        self.screen = screen

    def update(self) -> None:
        self.destroy_check()
        self.collision_check()

    def collision_check(self) -> None:
        # Loop through everything enemy collided with in this update.
        for enemy in pygame.sprite.spritecollide(self, self.enemy_ref, True):
            self.health -= enemy.get_damage()
            # print("Wall Health: ", self.health)

    def damage(self, intake) -> None:
        self.health -= intake
        # print(self.health)

    def destroy_check(self) -> None:
        if self.health <= 0:
            self.kill()

    def reset_to_initial(self) -> None:
        self.health = self.INITIAL_HEALTH
        self.max_health = self.INITIAL_MAX_HEALTH
        # self.rect = self.image.get_rect(topright=(self.screen.width / 2, 0))

    def set_variables(self, variables: dict):
        self.health = variables["health"]
        self.max_health = variables["max_health"]
