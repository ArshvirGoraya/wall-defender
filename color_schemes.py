from random import randint


class ColorScheme:
    '''
    This class stores color schemes.
    Generate color schemes at: https://coolors.co
    Scehmes are stored in a dictionary.
    Constants are hashed and point to colors for different components of the game.
    Currently point to strings which are hex codes used by Pygame for colors!

    Note:
    - Can probably store hex codes in a more efficient way (i.e., not as Strings).
    '''

    # Enum: color hash for each component.
    GROUND: int = 0
    AMMO: int = 1
    PLAYER: int = 2
    ENEMY: int = 3
    WALL: int = 4

    # Enum: All Schemes. Probably can store colors more efficiently (i.e., not as strings).
    S_WATERMELLON: dict = {
        GROUND: "#A7E8BD",
        AMMO: "#FFD972",
        PLAYER: "#C7EAE4",
        ENEMY: "#EFA7A7",
        WALL: "#EFA7A7",
    }
    S_BLUEBERRY: dict = {
        GROUND: "#F2FDFF",
        AMMO: "#564787",
        PLAYER: "#9AD4D6",
        ENEMY: "#DBCBD8",
        WALL: "#101935",
    }
    S_DARK: dict = {
        GROUND: "#2c3142",
        AMMO: "#505567",
        PLAYER: "#545b72",
        ENEMY: "#DBCBD8",
        WALL: "#393e51",
    }
    # DEFINE MORE COLOR SCHEMES HERE: ########################################

    current_scheme: dict = S_WATERMELLON

    def __init__(self, scheme) -> None:
        self.current_scheme = scheme

    def get_current_scheme(self) -> dict:
        return self.S_WATERMELLON

    def get_ground(self) -> str:
        return self.current_scheme[self.GROUND]

    def get_ammo(self) -> str:
        return self.current_scheme[self.AMMO]

    def get_player(self) -> str:
        return self.current_scheme[self.PLAYER]

    def get_enemy(self) -> str:
        return self.current_scheme[self.ENEMY]

    def get_wall(self) -> str:
        return self.current_scheme[self.WALL]

    # RGB randomization
    def randomize(self) -> None:
        # rgb = (randint(0, 255), randint(0, 255), randint(0, 255))

        for color in self.current_scheme:
            self.current_scheme[color] = (randint(
                0, 255),
                randint(0, 255),
                randint(0, 255))

    # def mono_randomize(self) -> None:
    #     # note: this function does not work as intended often, but can produce good outcomes sometimes.
    #     # Should rewrite later to generate better color schemes.
    #     #
    #     # Randomly assign RGB colors to create monochromatic color scheme.
    #     # 1 of them will increment by a constant amount for each color.
    #     # Must increment from low enough to not go over 255.
    #     # Increments: constant_increment * color_count (i.e., self.current_scheme.__len__())
    #     # So the one that is changed will be set low enough to not go over that amount.

    #     INCREMENT = 50

    #     rand_rgb = randint(1, 3)

    #     rand_color_1 = randint(0, 255)
    #     rand_color_2 = randint(0, 255)
    #     rand_color_3 = randint(0, 255)

    #     required_space = 255 - (INCREMENT * self.current_scheme.__len__())

    #     # Required space must not be larger than 255!
    #     assert (required_space > 0, "Decrease INCREMENT in colors.mono_ranodom()!")

    #     if rand_rgb == 1:
    #         if rand_color_1 > required_space:
    #             rand_color_1 = randint(0, 255 - required_space)
    #     elif rand_rgb == 2:
    #         if rand_color_2 > required_space:
    #             rand_color_2 = randint(0, 255 - required_space)
    #     else:
    #         if rand_color_3 > required_space:
    #             rand_color_3 = randint(0, 255 - required_space)

    #     for color in self.current_scheme:
    #         if rand_rgb == 1:
    #             rand_color_1 = rand_color_1 + 25
    #         elif rand_rgb == 2:
    #             rand_color_2 = rand_color_2 + 25
    #         else:
    #             rand_color_3 = rand_color_3 + 25

    #         self.current_scheme[color] = rand_color_1, rand_color_2, rand_color_3
