import pygame
import random
# import array as arr  # Incase: don't want to use lists.
import time
from math import ceil
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
from menus.fail_menu import FailMenu
from menus.upgrade_menu import UpgradeMenu
#
from ui.health_bar import HealthBar
#
from wave_emitter import WaveEmitter


pygame.init()

# Window Info ###############################
pygame.display.set_caption("Wall Defender")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

# Screen Display ###########################
screen_w = 1920 * 0.8
screen_h = 1080 * 0.8
screen = pygame.display.set_mode((screen_w, screen_h))
# screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Colors
colors = ColorScheme(ColorScheme.S_DARK)
# colors.randomize()

# Player, Ammo, Wall, Enemies, Bullets, etc.
game_components = GameComponents(colors, screen)
wave_emitter = WaveEmitter(game_components)

# MENU STUFF ###############################s
start_menu = StartMenu(screen, colors)
start_menu_text = start_menu.menu
button_start_game = start_menu.button_start_game

win_menu = WinMenu(screen, colors)
win_menu_text = win_menu.menu
button_endless = win_menu.button

pause_menu = PauseMenu(screen, colors)
pause_menu_text = pause_menu.menu
button_resume = pause_menu.button

fail_menu = FailMenu(screen, colors)
fail_menu_text = fail_menu.menu
button_restart_0 = fail_menu.button
button_restart_last = fail_menu.button_last

upgrade_menu = UpgradeMenu(screen, colors)
upgrade_menu_title = upgrade_menu.menu

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
    "RED",
    pygame.Vector2(150, 26),  # size
    pygame.Vector2(20, 70),  # pos
    game_components.get_player().health,
    game_components.get_player().max_health
)
ui_wall_health = HealthBar(
    colors.get_text(),
    colors.get_player(),
    colors.get_enemy(),
    "RED",
    pygame.Vector2(150, 26),  # size
    pygame.Vector2(20, 70 + 30),  # pos
    game_components.get_wall().health,
    game_components.get_wall().max_health
)
ui_wave = Text(
    color=colors.get_text(),
    font_size=40,
    text=f'Wave: {wave_emitter.current_wave} / {
        wave_emitter.final_wave}',
    pos=pygame.Vector2(screen_w/2, 20),
    centered=True
)
ui_enemy_count = Text(
    color=colors.get_text(),
    font_size=40,
    text=f'Incoming: {wave_emitter.get_incoming_enemies()}',
    pos=pygame.Vector2(screen_w/2, 50),
    centered=True
)
ui_timer = Text(
    color=colors.get_text(),
    font_size=40,
    text=f'{wave_emitter.current_time * 1000}',
    pos=pygame.Vector2(screen_w/2, 80),
    centered=True
)
ui_wall_enter = Text(
    color=colors.get_text(),
    font_size=20,
    text=f'enter',
    pos=pygame.Vector2(game_components.get_player().rect.x,
                       game_components.get_player().rect.y),
    centered=False
)

ui.add(
    ui_ammo,
    ui_player_health,
    ui_wall_health,
    ui_wave,
    ui_enemy_count,
    ui_timer,
    ui_wall_enter
)

starting_text = pygame.sprite.Group()
STARTING_TEXT_SIZE = 40
# STARTING_TEXT_POS = pygame.Vector2(screen_w/2, screen_h/2)
STARTING_TEXT_CENTERED = True
starting_text.add(
    Text(
        color=colors.get_text(),
        font_size=STARTING_TEXT_SIZE,
        text=f'incoming enemies...',
        pos=pygame.Vector2(screen_w/2, screen_h/2),
        centered=STARTING_TEXT_CENTERED
    ),
    Text(
        color=colors.get_text(),
        font_size=STARTING_TEXT_SIZE,
        text=f'pick up ammo...',
        pos=pygame.Vector2(screen_w/2, screen_h/2 + (40 * 1)),
        centered=STARTING_TEXT_CENTERED
    ),
    Text(
        color=colors.get_text(),
        font_size=STARTING_TEXT_SIZE,
        text=f'destroy them...',
        pos=pygame.Vector2(screen_w/2, screen_h/2 + (40 * 2)),
        centered=STARTING_TEXT_CENTERED
    ),
    Text(
        color=colors.get_text(),
        font_size=STARTING_TEXT_SIZE,
        text=f'defend the wall...',
        pos=pygame.Vector2(screen_w/2, screen_h/2 + (40 * 3)),
        centered=STARTING_TEXT_CENTERED
    )
)
#######################################
# Delta Time:
clock = pygame.time.Clock()  # To limit frame rate.
previous_time = time.time()  # For delta time (frame-rate independent).


def game_start():
    spawn_ammo(random.randint(5, 10))


def spawn_ammo(amount):
    for x in range(0, amount):
        game_components.spawn_ammo()


def draw_game(screen: pygame.surface.Surface) -> None:
    screen.fill((colors.get_ground()))
    game_components.wall.draw(screen)
    game_components.enemy.draw(screen)
    game_components.ammo.draw(screen)
    game_components.player.draw(screen)
    game_components.bullet.draw(screen)
    draw_ui()


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

    update_ui()


def draw_ui():
    ui.draw(screen)
    # If waves are not active = game just started. display starting text.
    if not wave_emitter.active:
        starting_text.draw(screen)


def update_ui():
    global game_state
    if game_components.get_player() != None:
        ui_ammo.update_text(f'Ammo: {game_components.get_player().ammo_count} / {
            game_components.get_player().max_ammo}')

        ui_player_health.update(game_components.get_player(
        ).health, game_components.get_player().max_health)
    else:
        # If player is dead: fail
        game_state = FAIL

    if game_components.get_wall() != None:
        ui_wall_health.update(game_components.get_wall(
        ).health, game_components.get_wall().max_health)
    else:
        # If wall is dead: fail
        game_state = FAIL

    if not in_endless_mode:

        ui_wave.update_text(f'Wave: {wave_emitter.current_wave} / {
            wave_emitter.final_wave}')
    else:
        ui_wave.update_text(f'Wave: {wave_emitter.current_wave}')

    if wave_emitter.is_in_wave():
        ui_enemy_count.update_text(
            f'Amount: {game_components.enemy.__len__()}')
        ui_timer.update_text("")
    else:
        ui_enemy_count.update_text(
            f'Incoming: {wave_emitter.get_incoming_enemies()}')

        # autopep8: off # adds spaces after ':'
        ui_timer.update_text(f'00:%02d' % (ceil(wave_emitter.current_time)))
        # autopep8: on

    if game_components.get_player() != None and game_components.get_player().is_near_wall():
        ui_wall_enter.update_text("enter")

        ui_wall_enter.update_pos(pygame.Vector2(game_components.get_player().rect.x - 2,
                                                game_components.get_player().rect.y - 20))

    else:
        if ui_wall_enter.text != "":
            ui_wall_enter.update_text("")

# Restart ###############################


def restart_game(previous_wave=False):
    global ammo_spawn_rate, INITIAL_AMMO_SPAWN_RATE
    # Reset player health to initial.
    # Reset ammo to initial.

    # Despawn enemies and ammo:
    game_components.enemy.empty()
    game_components.ammo.empty()

    # Re-create player/wall (if needed) and assign initial health.
    if not game_components.get_player():
        game_components.create_player()
    if not game_components.get_wall():
        game_components.create_wall()

    if previous_wave:  # If on first wave, just restart
        if wave_emitter.current_wave - 1 == 0:
            previous_wave = False

    if previous_wave:
        wave_emitter.set_to_wave((wave_emitter.current_wave - 1))

        game_components.get_wall().set_variables(
            wave_emitter.get_wave_start_wall_vars()
        )

        game_components.get_player().set_variables(
            wave_emitter.get_wave_start_player_vars()
        )
        # Spawn appropariate amount of ammo for the coming wave:
        spawn_ammo(random.randint(
            int(wave_emitter.get_incoming_enemies() / 2),
            int(wave_emitter.get_incoming_enemies())))
    else:
        game_components.get_player().reset_to_initial()
        game_components.get_wall().reset_to_initial()
        game_components.reset_to_initial()
        wave_emitter.reset_to_initial()
        # Reset ammo timer
        ammo_spawn_rate = INITIAL_AMMO_SPAWN_RATE
        pygame.time.set_timer(event_ammo_spawn, ammo_spawn_rate)
        # Spawn ammo at game start:
        game_start()


def start_next_wave_count():
    wave_emitter.start_count_to_next_wave()
    spawn_ammo(random.randint(
        int(wave_emitter.get_incoming_enemies() / 2),
        int(wave_emitter.get_incoming_enemies())))

# UPGRADES ###############################


def prompt_upgrade(screen) -> bool:
    upgrade_menu_title.draw(screen)

    for button in upgrade_menu.buttons:
        button.update(screen)
        button.draw(screen)

        if button.sprite.detect_click():
            upgrade(button)
            return True

    return False

# For debugging upgrades:


def print_stats():
    # print(wave_emitter.current_wave, ": ammo_cap = ",
    #       game_components.get_player().max_ammo)
    # print(wave_emitter.current_wave, ": player health = ",
    #       game_components.get_player().max_health)
    # print(wave_emitter.current_wave, ": wall health = ",
    #       game_components.get_wall().max_health)
    # print(wave_emitter.current_wave, ": player speed = ",
    #       game_components.get_player().speed)
    # print(wave_emitter.current_wave, ": shoot speed = ",
    #       game_components.get_player().shoot_wait_millis)
    # print(wave_emitter.current_wave, ": ammo spawn rate = ", ammo_spawn_rate)
    # print(wave_emitter.current_wave, ": bullet speed = ",
    #       game_components.bullet_speed)
    pass


def upgrade(button):
    global ammo_spawn_rate
    match button:
        case upgrade_menu.ammo_cap:
            game_components.get_player().max_ammo += 10
        ##
        case upgrade_menu.health_player:
            game_components.get_player().max_health += 10
            game_components.get_player().health = game_components.get_player().max_health

        case upgrade_menu.health_wall:
            game_components.get_wall().max_health += 3
            game_components.get_wall().health = game_components.get_wall().max_health
        ##
        case upgrade_menu.speed_up:
            game_components.get_player().speed += 10

        case upgrade_menu.speed_shoot:
            game_components.get_player().shoot_wait_millis -= 0.05

        case upgrade_menu.ammo_spawn_rate:
            ammo_spawn_rate = max(0, ammo_spawn_rate - 10)
            # Emit event on timer.
            pygame.time.set_timer(event_ammo_spawn, ammo_spawn_rate)

        ##
        case upgrade_menu.speed_bullet:
            game_components.bullet_speed += 50

        # case upgrade_menu.turret:
        #     pass
# CUSTOM EVENTS ###############################
event_ammo_spawn = pygame.USEREVENT + 1
# event_enemy_spawn = pygame.USEREVENT + 2
INITIAL_AMMO_SPAWN_RATE = 1000
ammo_spawn_rate = INITIAL_AMMO_SPAWN_RATE
# Emit event on timer.
pygame.time.set_timer(event_ammo_spawn, ammo_spawn_rate)
# pygame.time.set_timer(event_enemy_spawn, 1000)  # Emit event on timer.

event_start_waves = pygame.USEREVENT + 2

# For testing:

TEST_WAVE: bool = False
SKIP_OPENING: bool = True

if TEST_WAVE:
    if not SKIP_OPENING:
        SKIP_OPENING = True
    # Start at specified wave:
    elapsed_waves = 25
    # Get random upgrades for player by amount of waves.
    for wave in range(0, elapsed_waves):
        upgrade(
            random.choice(
                [upgrade_menu.speed_bullet,
                 upgrade_menu.ammo_spawn_rate,
                 upgrade_menu.speed_shoot,
                 upgrade_menu.speed_up,
                 upgrade_menu.health_wall,
                 upgrade_menu.health_player,
                 upgrade_menu.ammo_cap]
            )
        )
    # Start with half ammo
    game_components.get_player().ammo_count = game_components.get_player().max_ammo / 2
    # Save Variables
    wave_emitter.set_wave_start_variables()
    # Print stats (chosen upgrades):
    print_stats()

    # Start the wave
    wave_emitter.current_wave = elapsed_waves


if SKIP_OPENING:
    pygame.time.set_timer(event_start_waves, 10)  # Emit event on timer.
else:
    pygame.time.set_timer(event_start_waves, 10000)  # Emit event on timer.

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

in_endless_mode: bool = False

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
                game_components.spawn_ammo()

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                if game_components.get_player() != None:
                    if game_components.get_player().move_state == game_components.get_player().NEAR_WALL:
                        # enter wall
                        game_components.get_player().enter_wall()
                    elif game_components.get_player().move_state == game_components.get_player().IN_WALL:
                        # exit wall
                        game_components.get_player().exit_wall()

            if event.type == event_start_waves:
                # setting to 0 deletes the event.
                pygame.time.set_timer(event_start_waves, 0)
                # print("starting waves!")
                starting_text.empty()
                # Start waves...
                wave_emitter.active = True

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
                    game_state = UPGRADE

    if game_state == GAME:
        draw_game(screen)
        update_game(delta)

        if wave_emitter.is_in_wave():
            # Check if wave has ended.
            if not game_components.enemy.__len__():
                # Check if won game:
                if not in_endless_mode:
                    if wave_emitter.current_wave == wave_emitter.final_wave:
                        game_state = WIN

                game_state = UPGRADE
                # start_next_wave_count()
        else:
            start_next_wave = wave_emitter.update_timer(delta)  # Spawns waves.
            if start_next_wave:
                print_stats()
                # On wave 15, make count down be higher.
                if wave_emitter.current_wave == 15:
                    wave_emitter.COUNT_DOWN = 5

    elif game_state == UPGRADE:
        draw_game(screen)
        screen.blit(bg, bg.get_rect())

        upgrade_picked = prompt_upgrade(screen)

        if upgrade_picked:
            wave_emitter.set_wave_start_variables()
            start_next_wave_count()
            # save variables AFTER upgrading.
            game_state = GAME

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
            in_endless_mode = True

    elif game_state == FAIL:
        draw_game(screen)
        screen.blit(bg, bg.get_rect())

        fail_menu_text.draw(screen)

        button_restart_0.update(screen)
        button_restart_0.draw(screen)

        button_restart_last.update(screen)
        button_restart_last.draw(screen)

        if button_restart_0.sprite.detect_click():
            restart_game()
            game_state = GAME
        elif button_restart_last.sprite.detect_click():
            restart_game(True)
            game_state = GAME

    elif game_state == START:
        screen.fill((colors.get_ground()))
        start_menu_text.draw(screen)
        button_start_game.update(screen)
        button_start_game.draw(screen)

        if button_start_game.sprite.detect_click():
            game_state = GAME
            game_start()

    pygame.display.update()
    # clock.tick(60)  # FPS limited
