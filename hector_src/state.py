from typing import Dict, Tuple, List, Set
from globals import PlayerType, CharacterColor, color_mappings, question_mappings
from Character import Character

def generate_state_from_server_question(question: Dict, player_type: PlayerType):
    data = question['data']
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
        None,
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
    ongoing_card: Character
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
            oc: Character,
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
        self.ongoing_card = Character(oc.color, oc.suspect, oc.position, oc.power_used)
        self.choose_to_reach_state = choose_to_reach_state
        self.question = question

    def generate_state(self):
        return self

