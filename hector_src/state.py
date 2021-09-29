from typing import Dict, Tuple, List, Set
from globals import PlayerType, CharacterColor, color_mappings, question_mappings
from Character import Character

def generate_state_from_server_question(question: Dict, player_type: PlayerType):
    data = question['data']
    game_state: Dict = question['game state']
    blocked = (game_state['blocked'][0], game_state['blocked'][1])
    suspects = []
    state = State(
        color_mappings[game_state['fantom']] if 'fantom' in game_state else -1,
        game_state['position_carlotta'],
        game_state['num_tour'],
        player_type,
        game_state['shadow'],
        blocked
    )
    return state

class State:
    fantom: int
    pos_carlotta: int
    exit: int = 22
    nbr_turn: int
    next_player: PlayerType
    shadow: int
    blocked: Tuple[int, int]
    suspect: Set[int]
    active_cards: Set[int]
    choose_to_reach_state: int
    question: int

    def __init__(
            self,
            fantom: int,
            pos_carlotta: int,
            nbr_turn: int,
            next_player: PlayerType,
            shadow: int,
            blocked: Tuple[int, int],
            suspect: Set[int],
            active_cards: Set[int],
            choose_to_reach_state: int,
            question: int
    ):
        self.fantom = fantom
        self.pos_carlotta = pos_carlotta
        self.nbr_turn = nbr_turn
        self.next_player = next_player
        self.shadow = shadow
        self.blocked = blocked
        self.suspect = suspect
        self.active_cards = active_cards
        self.choose_to_reach_state = choose_to_reach_state
        self.question = question

    def generate_state(self):

        return self

    def select_character(self):
        print('select_character:')
        return self

    def activate_white_power(self):
        print('activate_white_power:')
        return self

    def activate_purple_power(self):
        print('activate_purple_power:')
        return self

    def activate_brown_power(self):
        print('activate_brown_power:')
        return self

    def activate_grey_power(self):
        print('activate_grey_power:')
        return self

    def activate_blue_power(self):
        print('activate_blue_power:')
        return self

    def activate_pink_power(self):
        print('activate_pink_power:')
        return self

    def activate_black_power(self):
        print('activate_black_power:')
        return self

    def activate_red_power(self):
        print('activate_red_power:')
        return self

    def select_position(self):
        print('select_position:')
        return self

    def purple_character_power(self):
        print('purple_character_power:')
        return self

    def brown_character_power(self):
        print('brown_character_power:')
        return self

    def grey_character_power(self):
        print('grey_character_power:')
        return self

    def blue_character_power_room(self):
        print('blue_character_power_room:')
        return self

    def blue_character_power_exit(self):
        print('blue_character_power_exit:')
        return self

    def white_character_power_move_purple(self):
        print('white_character_power_move_purple:')
        return self

    def white_character_power_move_brown(self):
        print('white_character_power_move_brown:')
        return self

    def white_character_power_move_grey(self):
        print('white_character_power_move_grey:')
        return self

    def white_character_power_move_blue(self):
        print('white_character_power_move_blue:')
        return self

    def white_character_power_move_pink(self):
        print('white_character_power_move_pink:')
        return self

    def white_character_power_move_black(self):
        print('white_character_power_move_black:')
        return self

    def white_character_power_move_red(self):
        print('white_character_power_move_red:')
        return self
