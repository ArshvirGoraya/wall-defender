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
        self.current_scheme = {
            self.GROUND: (randint(0, 255), randint(0, 255), randint(0, 255)),
            self.AMMO: (randint(0, 255), randint(0, 255), randint(0, 255)),
            self.PLAYER: (randint(0, 255), randint(0, 255), randint(0, 255)),
            self.ENEMY: (randint(0, 255), randint(0, 255), randint(0, 255)),
            self.WALL: (randint(0, 255), randint(0, 255), randint(0, 255)),
        }
