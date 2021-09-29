from typing import Tuple
from globals import PlayerType
from Character import Character


class State:
    fantom: int
    pos_carlotta: int
    exit: int = 22
    nbr_turn: int
    next_player: PlayerType
    shadow: int
    blocked: Tuple[int, int]
    alibi_card: [int]
    suspect: {int}
    active_cards: {int}
    ongoing_card: Character
    last_action: int

    def __init__(
            self,
            fantom: int,
            pos_carlotta: int,
            nbr_turn: int,
            next_player: PlayerType,
            shadow: int,
            blocked: Tuple[int, int],
            alibi_card: [int],
            suspect: {int},
            active_cards: {int},
            oc: Character,
            last_action: int
    ):
        self.fantom = fantom
        self.pos_carlotta = pos_carlotta
        self.nbr_turn = nbr_turn
        self.next_player = next_player
        self.shadow = shadow
        self.blocked = blocked
        self.alibi_card = alibi_card
        self.suspect = suspect
        self.active_cards = active_cards
        self.ongoing_card = Character(oc.color, oc.suspect, oc.position, oc.power_used)
        self.last_action = last_action

    def generate_state(self):
        return self
