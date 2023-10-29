import pygame


class HealthBar(pygame.sprite.Sprite):
    PADDING = 10

    def __init__(self, color, bg_color, danger_color, extreme_danger_color, size, pos, maximum, val) -> None:
        super().__init__()

        self.size = size

        self.bar = pygame.surface.Surface((size.x, size.y))
        self.bar.fill(bg_color)

        self.bar_inner = pygame.surface.Surface(
            (size.x - self.PADDING, size.y - self.PADDING))

        self.bar_inner.fill(color)

        self.bar.blit(self.bar_inner, self.bar_inner.get_rect(
            center=(self.bar.get_rect().width/2, self.bar.get_rect().height/2)))

        self.image = self.bar
        self.rect = self.image.get_rect(topleft=(pos.x, pos.y))

        self.inner_width_max = size.x - self.PADDING
        self.val = val
        self.max = maximum

        self.color = color
        self.bg_color = bg_color
        self.danger_color = danger_color
        self.extreme_danger_color = extreme_danger_color

    def update(self, health, health_max) -> None:
        inner_bar_width = self.get_bar_value(
            health, health_max, self.inner_width_max)

        # print(inner_bar_width, " / ", self.inner_width_max)

        color = self.color
        if health <= health_max * 0.2:
            color = self.extreme_danger_color
        elif health <= health_max * 0.5:
            color = self.danger_color

        self.draw_bar(color, self.bg_color, self.size, inner_bar_width)

    def get_bar_value(self, health_value, health_max, bar_max):
        health_value = self.normalize_value(health_value, 0, health_max)
        health_bar_value = self.get_value_from_normalized(
            health_value, 0, bar_max)
        return health_bar_value

        # Normalize health value.

    def normalize_value(self, value, minimum, maximum):
        return (value - minimum) / (maximum - minimum)

        # Once normalized, convert to health bar size.
    def get_value_from_normalized(self, normalized_value, minimum, maximum):
        bar_range = maximum - minimum
        value = minimum + normalized_value * bar_range
        return value

    def draw_bar(self, color, bg_color, size, inner_bar_width):
        # Draw outer bar
        self.bar = pygame.surface.Surface((size.x, size.y))
        self.bar.fill(bg_color)

        # Draw inner bar:

        self.bar_inner = pygame.surface.Surface(
            (max(0, inner_bar_width), size.y - self.PADDING))
        self.bar_inner.fill(color)

        self.bar.blit(self.bar_inner, self.bar_inner.get_rect(
            midleft=(self.PADDING/2, self.bar.get_rect().height/2)))

        # self.bar.blit(self.bar_inner, self.bar_inner.get_rect())

        #
        self.image = self.bar
