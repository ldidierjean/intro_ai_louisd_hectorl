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

cm = {
    "pink": 0,
    "blue": 1,
    "purple": 2,
    "grey": 3,
    "white": 4,
    "black": 5,
    "red": 6,
    "brown": 7
}

qm = {
    "select character": 0,
    "activate purple power": 2,
    "activate white power": 4,
    "activate black power": 5,
    "activate brown power": 7,
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

shuffle = [[0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 4, 3, 5, 6, 7], [0, 1, 2, 5, 3, 4, 6, 7], [0, 1, 2, 6, 3, 4, 5, 7], [0, 1, 2, 7, 3, 4, 5, 6], [0, 1, 3, 4, 2, 5, 6, 7], [0, 1, 3, 5, 2, 4, 6, 7], [0, 1, 3, 6, 2, 4, 5, 7], [0, 1, 3, 7, 2, 4, 5, 6], [0, 1, 4, 5, 2, 3, 6, 7], [0, 1, 4, 6, 2, 3, 5, 7], [0, 1, 4, 7, 2, 3, 5, 6], [0, 1, 5, 6, 2, 3, 4, 7], [0, 1, 5, 7, 2, 3, 4, 6], [0, 1, 6, 7, 2, 3, 4, 5], [0, 2, 3, 4, 1, 5, 6, 7], [0, 2, 3, 5, 1, 4, 6, 7], [0, 2, 3, 6, 1, 4, 5, 7], [0, 2, 3, 7, 1, 4, 5, 6], [0, 2, 4, 5, 1, 3, 6, 7], [0, 2, 4, 6, 1, 3, 5, 7], [0, 2, 4, 7, 1, 3, 5, 6], [0, 2, 5, 6, 1, 3, 4, 7], [0, 2, 5, 7, 1, 3, 4, 6], [0, 2, 6, 7, 1, 3, 4, 5], [0, 3, 4, 5, 1, 2, 6, 7], [0, 3, 4, 6, 1, 2, 5, 7], [0, 3, 4, 7, 1, 2, 5, 6], [0, 3, 5, 6, 1, 2, 4, 7], [0, 3, 5, 7, 1, 2, 4, 6], [0, 3, 6, 7, 1, 2, 4, 5], [0, 4, 5, 6, 1, 2, 3, 7], [0, 4, 5, 7, 1, 2, 3, 6], [0, 4, 6, 7, 1, 2, 3, 5], [0, 5, 6, 7, 1, 2, 3, 4], [1, 2, 3, 4, 0, 5, 6, 7], [1, 2, 3, 5, 0, 4, 6, 7], [1, 2, 3, 6, 0, 4, 5, 7], [1, 2, 3, 7, 0, 4, 5, 6], [1, 2, 4, 5, 0, 3, 6, 7], [1, 2, 4, 6, 0, 3, 5, 7], [1, 2, 4, 7, 0, 3, 5, 6], [1, 2, 5, 6, 0, 3, 4, 7], [1, 2, 5, 7, 0, 3, 4, 6], [1, 2, 6, 7, 0, 3, 4, 5], [1, 3, 4, 5, 0, 2, 6, 7], [1, 3, 4, 6, 0, 2, 5, 7], [1, 3, 4, 7, 0, 2, 5, 6], [1, 3, 5, 6, 0, 2, 4, 7], [1, 3, 5, 7, 0, 2, 4, 6], [1, 3, 6, 7, 0, 2, 4, 5], [1, 4, 5, 6, 0, 2, 3, 7], [1, 4, 5, 7, 0, 2, 3, 6], [1, 4, 6, 7, 0, 2, 3, 5], [1, 5, 6, 7, 0, 2, 3, 4], [2, 3, 4, 5, 0, 1, 6, 7], [2, 3, 4, 6, 0, 1, 5, 7], [2, 3, 4, 7, 0, 1, 5, 6], [2, 3, 5, 6, 0, 1, 4, 7], [2, 3, 5, 7, 0, 1, 4, 6], [2, 3, 6, 7, 0, 1, 4, 5], [2, 4, 5, 6, 0, 1, 3, 7], [2, 4, 5, 7, 0, 1, 3, 6], [2, 4, 6, 7, 0, 1, 3, 5], [2, 5, 6, 7, 0, 1, 3, 4], [3, 4, 5, 6, 0, 1, 2, 7], [3, 4, 5, 7, 0, 1, 2, 6], [3, 4, 6, 7, 0, 1, 2, 5], [3, 5, 6, 7, 0, 1, 2, 4], [4, 5, 6, 7, 0, 1, 2, 3]]

# from state import State;from globals import *;
# s = State(1, 1, 1, 1, 1, [1, 1], {1, 2, 3}, {1, 2, 3}, 1, 1, 1, [])

# fantom: int  # Color of the fantom
# pos_carlotta: int  # Position of carlotta
# exit: int = 22  # Position to reach the exit
# nbr_turn: int  # The number of the current turn
# next_player: PlayerType  # Who play next
# shadow: int  # Which room is in the dark
# blocked: Tuple[int, int]  # Which room are blocked
# suspect: Set[int]  # Who are the current suspects
# active_cards: Set[int]  # What card are waiting to be played
# choose_to_reach_state: int  # The option we need to do to reach the described state
# question: int  # The question asked and the next to ask
# ongoing_card: int  # Which card is currently being played
# positions: Dict[int, int]  # The position of the card [color, position]
# power_activated: Dict[int, bool]  # If the power where used this turn [color, bool]
# has_moved: Set[int]  # char who has moved this turn


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


minimax_depth_level = 5

x = {
    'game state': {
        'position_carlotta': 6,
        'exit': 22, 'num_tour': 1, 'shadow': 3, 'blocked': (0, 1),
        'characters': [{'color': 'white', 'suspect': True, 'position': 2, 'power': False},
                       {'color': 'pink', 'suspect': True, 'position': 2, 'power': False},
                       {'color': 'brown', 'suspect': True, 'position': 7, 'power': False},
                       {'color': 'purple', 'suspect': True, 'position': 7, 'power': False},
                       {'color': 'black', 'suspect': True, 'position': 4, 'power': False},
                       {'color': 'blue', 'suspect': True, 'position': 0, 'power': False},
                       {'color': 'red', 'suspect': True, 'position': 9, 'power': False},
                       {'color': 'grey', 'suspect': True, 'position': 3, 'power': False}],
        'character_cards': [{'color': 'black', 'suspect': True, 'position': 4, 'power': False},
                            {'color': 'purple', 'suspect': True, 'position': 7, 'power': False},
                            {'color': 'blue', 'suspect': True, 'position': 0, 'power': False},
                            {'color': 'white', 'suspect': True, 'position': 2, 'power': False},
                            {'color': 'grey', 'suspect': True, 'position': 3, 'power': False},
                            {'color': 'pink', 'suspect': True, 'position': 2, 'power': False},
                            {'color': 'brown', 'suspect': True, 'position': 7, 'power': False},
                            {'color': 'red', 'suspect': True, 'position': 9, 'power': False}],
        'active character_cards': []
    },
    'question type': "select character"

}
