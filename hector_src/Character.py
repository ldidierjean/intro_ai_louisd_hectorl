class Character:
    color: int
    is_suspect: bool
    position: int

    def __init__(
            self,
            color: int,
            suspect: bool = True,
            position: int = 0,
    ):
        self.color = color
        self.suspect = suspect
        self.position = position
