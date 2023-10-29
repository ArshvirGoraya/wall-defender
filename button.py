import pygame


class Button(pygame.sprite.Sprite):
    BG_PADDING = 10
    hovering: bool = False
    pressed: bool = False

    def __init__(self, color, bg_color, hover_bg_color, pressed_bg_color, disabled_bg_color, disabled, text, font_size, pos) -> None:
        super().__init__()

        self.disabled = disabled
        self.text = text

        self.color = color
        self.width = 30
        self.height = 30

        # Image
        font = pygame.font.Font('assets/monogram.ttf', int(font_size))
        self.image = font.render(self.text, True, color)

        # Rect
        self.pos = pos
        self.rect = self.image.get_rect(center=(pos.x, pos.y))

        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        self.pressed_bg_color = pressed_bg_color
        self.disabled_bg_color = disabled_bg_color

    def update(self, screen) -> None:
        self.draw_background(screen)
        # self.detect_click()

    # Called by event loop
    def detect_click(self) -> bool:
        if self.disabled:
            return False
        # Detects when button is pressed.
        # Must click button from inside and release from inside!
        # Can't click button if button is being held down from the outside coming in.
        clicked = False
        if self.hovering:
            if not self.pressed:
                if any(pygame.mouse.get_pressed()):
                    self.pressed = True
            else:  # if pressed and released while hover = clicked.
                if not any(pygame.mouse.get_pressed()):
                    self.pressed = False
                    clicked = True
                    # print("click")

        if not any(pygame.mouse.get_pressed()):
            self.pressed = False

        return clicked

    def draw_background(self, screen: pygame.surface.Surface) -> None:
        background_rect = self.rect.copy()
        background_rect.width += self.BG_PADDING
        background_rect.height += self.BG_PADDING
        background_rect.center = (self.pos.x, self.pos.y)

        color = self.bg_color
        # If mouse is over button:
        if background_rect.collidepoint(pygame.mouse.get_pos()):
            self.hovering = True
            color = self.hover_bg_color
        else:
            self.hovering = False

        if self.pressed:
            color = self.pressed_bg_color

        if self.disabled:
            color = self.disabled_bg_color

        pygame.draw.rect(screen, color, background_rect)
