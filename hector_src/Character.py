class Character:
    color: int
    is_suspect: bool
    position: int
    power_used: bool

    def __init__(
            self,
            color: int,
            suspect: bool = True,
            position: int = 0,
            power_used: bool = False
    ):
        self.color = color
        self.suspect = suspect
        self.position = position
        self.power_used = power_used
