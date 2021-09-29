from typing import Dict, Tuple, List, Set
from globals import PlayerType, CharacterColor, color_mappings, question_mappings
from Character import Character

def generate_state_from_server_question(question: Dict):
    data = question['data']
    game_state = question['game state']
    state = State(

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

