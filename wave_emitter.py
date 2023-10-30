import pygame
from game_components import GameComponents


class WaveEmitter():
    # states
    IN_WAVE = 0
    WAIT_WAVE = 1

    state = WAIT_WAVE

    current_wave = 0
    COUNT_DOWN = 2

    current_time = COUNT_DOWN  # counts down to 0

    final_wave = 100

    enemy_increment = 10

    game_components: GameComponents

    def __init__(self, game_components) -> None:
        self.game_components = game_components
        # self.set_wave_start_variables()

    def is_in_wave(self) -> bool:
        return self.state == self.IN_WAVE

    def start_wave(self):
        self.set_wave_start_variables()
        for x in range(0, self.get_incoming_enemies()):
            self.game_components.spawn_enemy()

    def get_incoming_enemies(self):
        return self.enemy_increment * (self.current_wave + 1)

    def update_timer(self, delta,):
        if self.state == self.IN_WAVE:  # Timer should not increment while in wave.
            return

        self.current_time = max(0, self.current_time - delta)

        if self.current_time <= 0:
            self.state = self.IN_WAVE
            self.start_wave()
            self.current_wave += 1  # Make sure this is below start_wave!

    def start_count_to_next_wave(self):
        # print("counting to next wave!")
        self.current_time = self.COUNT_DOWN
        self.state = self.WAIT_WAVE

    def reset_to_initial(self) -> None:
        self.state = self.WAIT_WAVE
        self.current_time = self.COUNT_DOWN
        self.current_wave = 0

    def set_to_wave(self, wave_num) -> None:
        self.state = self.WAIT_WAVE
        self.current_time = self.COUNT_DOWN
        self.current_wave = max(0, wave_num)  # cant go below 0

    def set_wave_start_variables(self):
        self.wave_start_wall_variables = {
            "health": self.game_components.get_wall().health,
            "max_health": self.game_components.get_wall().max_health,
        }
        self.wave_start_player_variables = {
            "health": self.game_components.get_player().health,
            "max_health": self.game_components.get_player().max_health,
            "ammo_count": self.game_components.get_player().ammo_count,
            "max_ammo": self.game_components.get_player().max_ammo,
            "speed": self.game_components.get_player().speed,
            "shoot_wait_millis": self.game_components.get_player().shoot_wait_millis,
        }

    def get_wave_start_player_vars(self) -> dict:
        return self.wave_start_player_variables

    def get_wave_start_wall_vars(self) -> dict:
        return self.wave_start_wall_variables
