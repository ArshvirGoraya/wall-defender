import pygame
from game_components import GameComponents


class WaveEmitter():
    # states
    IN_WAVE = 0
    WAIT_WAVE = 1

    state = WAIT_WAVE

    current_wave = 0
    current_time = 0
    WAIT_TIMER = 1  # secs

    enemy_increment = 10

    def is_in_wave(self) -> bool:
        return self.state == self.IN_WAVE

    def start_wave(self, game_components: GameComponents):
        print("STARTING WAVE!")
        for x in range(1, self.get_incoming_enemies()):
            game_components.spawn_enemy()

    def get_incoming_enemies(self):
        return self.enemy_increment * self.current_wave + 1

    def update_timer(self, delta, game_components: GameComponents):
        if self.state == self.IN_WAVE:  # Timer should not increment while in wave.
            return

        self.current_time += delta

        if self.current_time >= self.WAIT_TIMER:
            self.current_wave += 1
            self.state = self.IN_WAVE
            self.start_wave(game_components)

            self.current_time = 0

    def start_count_to_next_wave(self):
        print("counting to next wave!")
        self.state = self.WAIT_WAVE
