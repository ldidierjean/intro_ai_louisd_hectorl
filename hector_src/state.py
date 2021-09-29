from typing import Dict, Tuple, List, Set
from globals import PlayerType, CharacterColor, color_mappings, question_mappings
from Character import Character
import copy

def generate_state_from_server_question(question: Dict, player_type: PlayerType):
    game_state: Dict = question['game state']
    blocked = (game_state['blocked'][0], game_state['blocked'][1])
    suspects: Set[int] = set()
    active_cards: Set[int] = set()

    for character in game_state['characters']:
        if character['suspect'] == True:
            suspects.add(color_mappings[character['color']])

    for card in game_state['active character_cards']:
        active_cards.add(color_mappings[card['color']])

    state = State(
        color_mappings[game_state['fantom']] if 'fantom' in game_state else -1,
        game_state['position_carlotta'],
        game_state['num_tour'],
        player_type,
        game_state['shadow'],
        blocked,
        suspects,
        active_cards,
        -1,
        question_mappings[question['question']]
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
    ongoing_card: int

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
            question: int,
            ongoing_card: int
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
        self.ongoing_card = ongoing_card

    def __repr__(self):
        return "Fantom: " + str(self.fantom) + \
            "\npos_carlotta: " + str(self.pos_carlotta) + \
            "\nnbr_turn: " + str(self.nbr_turn) + \
            "\nnext_player: " + str(self.next_player) + \
            "\nshadow: " + str(self.shadow) + \
            "\nblocked: " + str(self.blocked) + \
            "\nsuspect: " + str(self.suspect) + \
            "\nactive_cards: " + str(self.active_cards) + \
            "\nchoose_to_reach_state: " + str(self.choose_to_reach_state) + \
            "\nquestion: " + str(self.question)


    def generate_state(self):
        switcher = {
            0: self.select_character,
            1: self.activate_white_power,
            2: self.activate_purple_power,
            3: self.activate_brown_power,
            4: self.activate_grey_power,
            5: self.activate_blue_power,
            6: self.activate_pink_power,
            7: self.activate_black_power,
            8: self.activate_red_power,
            9: self.select_position,
            10: self.purple_character_power,
            11: self.brown_character_power,
            12: self.grey_character_power,
            13: self.blue_character_power_room,
            14: self.blue_character_power_exit,
            15: self.white_character_power_move_purple,
            16: self.white_character_power_move_brown,
            17: self.white_character_power_move_grey,
            18: self.white_character_power_move_blue,
            19: self.white_character_power_move_pink,
            20: self.white_character_power_move_black,
            21: self.white_character_power_move_red
        }
        switcher.get(self.question)()
        return self

    def select_character(self):
        print('select_character:')
        nextStates = []
        for c in self.active_cards:
            copy = copy.deepcopy(self)
            copy.
            nextStates.append()
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
