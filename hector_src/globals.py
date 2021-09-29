from enum import Enum

"""
    game data
"""
# determines whether the power of the character is used before
# or after moving
permanents = {"pink"}
before = {"purple", "brown"}
after = {"black", "white", "red", "blue", "grey"}

# reunion of sets
colors = {"pink",
          "blue",
          "purple",
          "grey",
          "white",
          "black",
          "red",
          "brown"}

# ways between rooms
# rooms are numbered
# from right to left
# from bottom to top
# 0 ---> 9
passages = [{1, 4}, {0, 2}, {1, 3}, {2, 7}, {0, 5, 8},
            {4, 6}, {5, 7}, {3, 6, 9}, {4, 9}, {7, 8}]
# ways for the pink character
pink_passages = [{1, 4}, {0, 2, 5, 7}, {1, 3, 6}, {2, 7}, {0, 5, 8, 9},
                 {4, 6, 1, 8}, {5, 7, 2, 9}, {3, 6, 9, 1}, {4, 9, 5},
                 {7, 8, 4, 6}]

mandatory_powers = ["red", "blue", "grey"]

color_mappings = {
    "pink": 0,
    "blue": 1,
    "purple": 2,
    "grey": 3,
    "white": 4,
    "black": 5,
    "red": 6,
    "brown": 7
}

question_mappings = {
    "select character": 0,
    "activate white power": 1,
    "activate purple power": 2,
    "activate brown power": 3,
    "activate grey power": 4,
    "activate blue power": 5,
    "activate black power": 7,
    "select position": 9,
    "purple character power": 10,
    "brown character power": 11,
    "grey character power": 12,
    "blue character power room": 13,
    "blue character power exit": 14,
    "white character power move purple": 15,
    "white character power move brown": 16,
    "white character power move grey": 17,
    "white character power move blue": 18,
    "white character power move pink": 19,
    "white character power move black": 20,
    "white character power move red": 21
}

class PlayerType(Enum):
    FANTOM = 0
    INSPECTOR = 1


class CharacterColor(Enum):
    PINK = 0
    BLUE = 1
    PURPLE = 2
    GREY = 3
    WHITE = 4
    BLACK = 5
    RED = 6
    BROWN = 7


minimax_depth_level = 8
