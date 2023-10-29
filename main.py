import pygame
import random
# import array as arr  # Incase: don't want to use lists.
import time
#
from color_schemes import ColorScheme
from game_components import GameComponents
#
# from button import Button
from menus.text import Text
#
from menus.start_menu import StartMenu
from menus.win_menu import WinMenu
from menus.pause_menu import PauseMenu
#
from ui.health_bar import HealthBar


pygame.init()

# Window Info ###############################
pygame.display.set_caption("Resource Defender")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

# Screen Display ###########################
screen_w = 1920 * 0.8
screen_h = 1080 * 0.8
# screen = pygame.display.set_mode((screen_w, screen_h))
screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Colors
colors = ColorScheme(ColorScheme.S_DARK)
# colors.randomize()

# Player, Ammo, Wall, Enemies, Bullets, etc.
game_components = GameComponents(colors, screen)


# CUSTOM EVENTS & TIMERS ###############################
event_ammo_spawn = pygame.USEREVENT + 1
event_enemy_spawn = pygame.USEREVENT + 2

ammo_timer = pygame.time.set_timer(event_ammo_spawn, 1000)
enemy_timer = pygame.time.set_timer(event_enemy_spawn, 1000)

# MENU STUFF ###############################
start_menu = StartMenu(screen, colors)
start_menu_text = start_menu.menu
button_start_game = start_menu.button_start_game

win_menu = WinMenu(screen, colors)
win_menu_text = win_menu.menu
button_endless = win_menu.button

pause_menu = PauseMenu(screen, colors)
pause_menu_text = pause_menu.menu
button_resume = pause_menu.button

# Background fill with opacity. Can be used in many places.
bg = pygame.surface.Surface(screen.get_size())
bg.fill((colors.get_ground()))
bg.set_alpha(100)
# UI STUFF ###############################
# ammo_string = f'ammo: {b}'

ui = pygame.sprite.Group()

ui_ammo = Text(
    color=colors.get_text(),
    font_size=40,
    text=f'Ammo: {game_components.get_player().ammo_count} / {
        game_components.get_player().max_ammo}',
    pos=pygame.Vector2(20, 20),
    centered=False
)
ui_player_health = HealthBar(
    colors.get_text(),
    colors.get_player(),
    colors.get_enemy(),
    pygame.Vector2(150, 26),  # size
    pygame.Vector2(20, 70),  # pos
    game_components.get_player().health,
    game_components.get_player().max_health
)

ui.add(
    ui_ammo,
    ui_player_health
)


#######################################
# Delta Time:
clock = pygame.time.Clock()  # To limit frame rate.
previous_time = time.time()  # For delta time (frame-rate independent).


def game_start():
    # Inital ammo
    for x in range(random.randint(5, 10)):
        game_components.spawn_ammo()


def draw_game(screen: pygame.surface.Surface) -> None:
    screen.fill((colors.get_ground()))
    game_components.wall.draw(screen)
    game_components.enemy.draw(screen)
    game_components.ammo.draw(screen)
    game_components.player.draw(screen)
    game_components.bullet.draw(screen)


def update_game(delta) -> None:
    game_components.wall.update()
    game_components.enemy.update(delta)

    # Ammo resources on the ground.
    game_components.ammo.update(delta)
    game_components.player.update(delta)

    # Update all spawned bullets:
    game_components.bullet.update(delta)

    # Spawn bullet if player has shot:
    # If player has ammo,
    # check if is shooting and get direction of shot.
    if game_components.player.sprite != None:  # Check if player is not dead.
        if game_components.player.sprite.ammo_count:
            bullet_direction = game_components.player.sprite.shooting()
            if bullet_direction.length() != 0:
                game_components.spawn_bullet(bullet_direction)


# Game States ###############################
# Enum: Game States (don't want/need enum import)
GAME = 0
START = 1
PAUSE = 2
FAIL = 3
WIN = 4
UPGRADE = 5

game_state = START
unpause_game_state = game_state
while True:
    delta = time.time() - previous_time
    previous_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  # Exits while loop immediately.

        # When in game:
        if game_state == GAME:
            # Match case is kind of annoying in python: can't just match with event_ammo_spawn
            if event.type == event_ammo_spawn:
                game_components. spawn_ammo()

            elif event.type == event_enemy_spawn:
                game_components.spawn_enemy()

        # When not in start menu (escape menu access)
        if game_state != START:
            # On escape pressed:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state == PAUSE:
                    game_state = unpause_game_state
                else:
                    unpause_game_state = game_state
                    game_state = PAUSE

            # TESTING:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = FAIL

    if game_state == GAME:
        draw_game(screen)
        update_game(delta)

    elif game_start == UPGRADE:
        pass

    elif game_state == PAUSE:
        draw_game(screen)
        screen.blit(bg, bg.get_rect())
        pause_menu_text.draw(screen)
        button_resume.update(screen)
        button_resume.draw(screen)
        if button_resume.sprite.detect_click():
            game_state = unpause_game_state

    elif game_state == WIN:
        draw_game(screen)
        screen.blit(bg, bg.get_rect())
        win_menu_text.draw(screen)
        button_endless.update(screen)
        button_endless.draw(screen)
        if button_endless.sprite.detect_click():
            game_state = GAME

    elif game_state == FAIL:
        pass

    elif game_state == START:
        screen.fill((colors.get_ground()))
        start_menu_text.draw(screen)
        button_start_game.update(screen)
        button_start_game.draw(screen)
        if button_start_game.sprite.detect_click():
            game_state = GAME
            game_start()

    if game_components.get_player() != None:
        ui_ammo.update_text(f'Ammo: {game_components.get_player().ammo_count} / {
            game_components.get_player().max_ammo}')

        ui_player_health.update(game_components.get_player(
        ).health, game_components.get_player().max_health)

    ui.draw(screen)

    pygame.display.update()
    clock.tick(60)  # FPS limited
