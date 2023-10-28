class ColorScheme:
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

    current_scheme: dict = S_WATERMELLON

    def __init__(self, scheme) -> None:
        self.current_scheme = scheme

    def get_current_scheme(self) -> dict:
        return self.S_WATERMELLON

    def get_ground(self):
        return self.current_scheme[self.GROUND]

    def get_ammo(self):
        return self.current_scheme[self.AMMO]

    def get_player(self):
        return self.current_scheme[self.PLAYER]

    def get_enemy(self):
        return self.current_scheme[self.ENEMY]

    def get_wall(self):
        return self.current_scheme[self.WALL]
