from typing import Dict, Tuple, List, Set
from hector_src.globals import PlayerType, CharacterColor, cm, qm, passages, pink_passages, shuffle
from hector_src.Character import Character
import copy
import itertools

def generate_state_from_server_question(question: Dict, player_type: PlayerType, current_ongoing_card: int):
    game_state: Dict = question['game state']
    blocked = (game_state['blocked'][0], game_state['blocked'][1])
    suspects: Set[int] = set()
    character_cards: Set[int] = set()
    active_cards: Set[int] = set()
    positions: Dict[int, int] = dict()

    for character in game_state['characters']:
        if character['suspect']:
            suspects.add(cm[character['color']])
        positions[cm[character['color']]] = character['position']

    for card in game_state['character_cards']:
        character_cards.add(cm[card['color']])

    for card in game_state['active character_cards']:
        active_cards.add(cm[card['color']])

    state = State(
        cm[game_state['fantom']] if 'fantom' in game_state else -1,
        game_state['position_carlotta'],
        game_state['num_tour'],
        player_type,
        game_state['shadow'],
        blocked,
        suspects,
        character_cards,
        active_cards,
        -1,
        qm[question['question type']],
        current_ongoing_card,
        positions
    )
    return state


# TODO: when select character is called and active card is empty:

class State:
    fantom: int  # Color of the fantom
    pos_carlotta: int  # Position of carlotta
    exit: int = 22  # Position to reach the exit
    nbr_turn: int  # The number of the current turn
    next_player: PlayerType  # Who play next
    shadow: int  # Which room is in the dark
    blocked: Tuple[int, int]  # Which room are blocked
    suspect: Set[int]  # Who are the current suspects
    character_cards: Set[int]  # All card shuffled
    active_cards: Set[int]  # What card are waiting to be played
    choose_to_reach_state: int  # The option we need to do to reach the described state
    question: int  # The question asked and the next to ask
    ongoing_card: int  # Which card is currently being played
    positions: Dict[int, int]  # The position of the card [color, position]
    power_activated: Set[int]  # If the power where used this turn
    has_moved: Set[int]  # char who has moved this turn

    def __init__(
            self,
            fantom: int,
            pos_carlotta: int,
            nbr_turn: int,
            next_player: PlayerType,
            shadow: int,
            blocked: Tuple[int, int],
            suspect: Set[int],
            character_cards: Set[int],
            active_cards: Set[int],
            choose_to_reach_state: int,
            question: int,
            ongoing_card: int,
            positions: Dict[int, int],
            power_activated: Set[int] = None,
            has_moved: Set[int] = None
    ):
        self.fantom = fantom
        self.pos_carlotta = pos_carlotta
        self.nbr_turn = nbr_turn
        self.next_player = next_player
        self.shadow = shadow
        self.blocked = blocked
        self.suspect = suspect
        self.character_cards = character_cards
        self.active_cards = active_cards
        self.choose_to_reach_state = choose_to_reach_state
        self.question = question
        self.ongoing_card = ongoing_card
        self.positions = positions
        self.power_activated = set() if power_activated is None else power_activated
        self.has_moved = set() if has_moved is None else has_moved

    def __repr__(self):
        return "\n\nState: " \
               "\n  Fantom: " + str(self.fantom) + \
               "\n  pos_carlotta: " + str(self.pos_carlotta) + \
               "\n  nbr_turn: " + str(self.nbr_turn) + \
               "\n  next_player: " + str(self.next_player) + \
               "\n  shadow: " + str(self.shadow) + \
               "\n  blocked: " + str(self.blocked) + \
               "\n  suspect: " + str(self.suspect) + \
               "\n  character_cards: " + str(self.character_cards) + \
               "\n  active_cards: " + str(self.active_cards) + \
               "\n  choose_to_reach_state: " + str(self.choose_to_reach_state) + \
               "\n  question: " + str(self.question) + \
               "\n  ongoing_card: " + str(self.ongoing_card) + \
               "\n  Position: " + str(self.positions) + \
               "\n  power_activated: " + str(self.power_activated)


    def handle_fantom_scream(self, state):
        partition: List[Set[Character]] = [
            {p for p in state.positions if state.positions[p] == i} for i in range(10)]
        if len(partition[state.positions[state.fantom]]) == 1 \
                or state.positions[state.fantom] == state.shadow:
            state.pos_carlotta += 1
            for room, chars in enumerate(partition):
                if len(chars) > 1 and room != state.shadow:
                    for p in chars:
                        state.suspect.remove(p)
        else:
            for room, chars in enumerate(partition):
                if len(chars) == 1 or room == state.shadow:
                    for p in chars:
                        state.suspect.remove(p)
        state.pos_carlotta += len(state.suspect)
        return state

    def handle_play_end(self, base_state):
        copied_state = copy.deepcopy(base_state)
        if len(base_state.active_cards) == 0:
            copied_state.nbr_turn += 1
        p = (copied_state.nbr_turn + 1) % 2
        idx = [p, 1-p, 1-p, p][3 - len(copied_state.active_cards)]
        copied_state.next_player = [PlayerType.FANTOM, PlayerType.INSPECTOR][idx]
        if len(base_state.active_cards) == 0:
            copied_state = self.handle_fantom_scream(copied_state)
            if p == 0:
                s = []
                for x in shuffle:
                    ns = copy.deepcopy(copied_state)
                    ns.character_cards = x
                    ns.active_cards = x[:4]
                    s.append(ns)
                return [s]
            else:
                copied_state.active_cards = copied_state.character_cards[4:]
                return [copied_state]
        else:
            return [copied_state]

    def generate_state(self):
        switcher = {
            qm["select character"]: self.select_character,
            qm["activate purple power"]: self.activate_purple_power,
            qm["activate white power"]: self.activate_white_power,
            qm["activate black power"]: self.activate_black_power,
            qm["activate brown power"]: self.activate_brown_power,
            qm["select position"]: self.select_position,
            qm["purple character power"]: self.purple_character_power,
            qm["brown character power"]: self.brown_character_power,
            qm["grey character power"]: self.grey_character_power,
            qm["blue character power room"]: self.blue_character_power_room,
            qm["blue character power exit"]: self.blue_character_power_exit,
            qm["white character power move purple"]: self.white_character_power_move_purple,
            qm["white character power move brown"]: self.white_character_power_move_brown,
            qm["white character power move grey"]: self.white_character_power_move_grey,
            qm["white character power move blue"]: self.white_character_power_move_blue,
            qm["white character power move pink"]: self.white_character_power_move_pink,
            qm["white character power move black"]: self.white_character_power_move_black,
            qm["white character power move red"]: self.white_character_power_move_red
        }
        new_states = []
        for ns in switcher.get(self.question)():
            if ns.question == qm["select character"]:
                new_states += self.handle_play_end(ns)
            else:
                new_states += ns
        return new_states

    # Next action
    #   Pink: select position
    #   Blue: select position or activate blue power
    #   Purple: select position or activate purple power
    #   Grey: select position or activate grey power
    #   White: select position
    #   Black: select position
    #   Red: select position
    #   Brown: select position

    def select_character(self):
        # print(f"Select Character: {self}")
        next_states = []
        for c in self.active_cards:
            ns = copy.deepcopy(self)
            ns.active_cards.remove(c)
            ns.ongoing_card = c
            ns.choose_to_reach_state = c
            ns.question = qm["select position"]
            next_states.append(ns)
            if c in [cm['blue'], cm['purple'], cm['grey']]:
                ns2 = copy.deepcopy(ns)
                powers = {
                    cm['blue']: qm['blue character power room'],
                    cm['purple']: qm['activate purple power'],
                    cm['grey']: qm['grey character power']
                }
                ns2.question = powers[c]
                next_states.append(ns2)
        return next_states

    # TODO: handle white power
    def activate_white_power(self):
        # print('activate_white_power:')
        ns = copy.deepcopy(self)
        ns.power_activated.add(cm['white'])
        #ns.question = qm['white character power']
        return [ns]

    def activate_purple_power(self):
        ns = copy.deepcopy(self)
        ns.power_activated.add(cm['purple'])
        ns.question = qm['purple character power']
        return [ns]

    def activate_brown_power(self):
        ns = copy.deepcopy(self)
        ns.power_activated.add(cm['brown'])
        ns.question = qm['brown character power']
        return [ns]

    def activate_black_power(self):
        # print(f'activate_black_power: {self}')
        r = self.get_adjacent_pos(passages, self.positions[self.ongoing_card])
        for p in self.positions:
            if self.positions[p] in r:
                self.positions[p] = self.positions[self.ongoing_card]
        ns = copy.deepcopy(self)
        ns.question = qm['select character']
        return [ns]

    def get_adjacent_pos(self, pa, pos):
        return [room for room in pa[pos] if {room, pos} != set(self.blocked)]

    # Next action
    #   Pink: select character
    #   Blue: si power_activated[blue] -> select character sinon -> activate blue power
    #   Purple: select character
    #   Grey: si power_activated[grey] -> select character sinon -> activate grey power
    #   White: select_character or activate white power
    #   Black: select_character or activate black power
    #   Red: activate red power
    #   Brown: select_character or activate brown power
    #   TODO: handle red power

    def select_position(self):
        # print(f'Select_position: {self}')
        # Passages available
        pa = (pink_passages if self.ongoing_card == cm["pink"] else passages)
        pos = self.positions[self.ongoing_card]
        # Number of character in room
        ncir = len([c for c in self.positions.values() if c == pos])
        choices = list()
        choices.append(self.get_adjacent_pos(pa, pos))
        for step in range(1, ncir):
            next_choices = list()
            for r in choices[step - 1]:
                next_choices += self.get_adjacent_pos(pa, r)
            choices.append(next_choices)
        tmp = list()
        for sublist in choices:
            for room in sublist:
                tmp.append(room)
        tmp = set(tmp)
        choices = list(tmp)
        if pos in choices:
            choices.remove(pos)
        next_states = []
        for c in choices:
            ns = copy.deepcopy(self)
            ns.positions[self.ongoing_card] = c
            ns.has_moved.add(self.ongoing_card)
            if self.ongoing_card in [cm['pink'], cm['purple'], cm['white'], cm['black'], cm['brown']]:
                ns.question = qm['select character']
            if self.ongoing_card == cm['blue']:
                ns.question = (qm['select character'] if self.ongoing_card in self.power_activated else
                               qm['blue character power room'])
            if self.ongoing_card == cm['grey']:
                ns.question = (qm['select character'] if self.ongoing_card in self.power_activated else
                               qm['grey character power'])
            ns.choose_to_reach_state = c
            next_states.append(ns)
            if self.ongoing_card in [cm['white'], cm['black'], cm['brown']]:
                ns2 = copy.deepcopy(self)
                q = {
                    cm['white']: qm['activate white power'],
                    cm['black']: qm['activate black power'],
                    cm['brown']: qm['activate brown power']
                }
                ns2.question = q[self.ongoing_card]
                ns2.choose_to_reach_state = c
                next_states.append(ns2)
        return next_states

    def purple_character_power(self):
        # print(f'purple_character_power: {self}')
        question = (qm['select character'] if self.ongoing_card in self.has_moved else
                    qm['select position'])
        next_states = []
        for c in range(8):
            if c == cm['purple']:
                continue
            ns = copy.deepcopy(self)
            ns.question = question
            ns.choose_to_reach_state = c
            purple_pos = ns.positions[cm['purple']]
            ns.positions[cm['purple']] = ns.positions[c]
            ns.positions[c] = purple_pos
            next_states.append(ns)
        return next_states

    # TODO: handle brown power
    def brown_character_power(self):
        #print('brown_character_power:')
        return [copy.deepcopy(self)]

    def grey_character_power(self):
        # print(f'grey_character_power: {self}')
        question = (qm['select character'] if self.ongoing_card in self.has_moved else
                    qm['select position'])
        next_states = []
        for c in range(10):
            if c == self.shadow:
                continue
            ns = copy.deepcopy(self)
            ns.power_activated.add(cm['grey'])
            ns.question = question
            ns.choose_to_reach_state = c
            ns.shadow = c
            next_states.append(ns)
        return next_states

    def blue_character_power_room(self):
        # print(f'blue_character_power_room: {self}')
        next_states = []
        for c in range(10):
            if c in self.blocked:
                continue
            ns = copy.deepcopy(self)
            ns.question = qm['blue character power exit']
            ns.choose_to_reach_state = c
            ns.blocked = tuple((c, ns.blocked[1]))
            next_states.append(ns)
        return next_states

    def blue_character_power_exit(self):
        # print(f'blue_character_power_exit: {self}')
        next_states = []
        question = (qm['select character'] if self.ongoing_card in self.has_moved else
                    qm['select position'])
        for c in range(10):
            if c == self.blocked[0]:
                continue
            ns = copy.deepcopy(self)
            ns.power_activated.add(cm['blue'])
            ns.question = question
            ns.choose_to_reach_state = c
            ns.blocked = tuple((ns.blocked[0], c))
            next_states.append(ns)
        return next_states

    def white_character_power_move_purple(self):
        #print('white_character_power_move_purple:')
        return [copy.deepcopy(self)]

    def white_character_power_move_brown(self):
        #print('white_character_power_move_brown:')
        return [copy.deepcopy(self)]

    def white_character_power_move_grey(self):
        #print('white_character_power_move_grey:')
        return [copy.deepcopy(self)]

    def white_character_power_move_blue(self):
        #print('white_character_power_move_blue:')
        return [copy.deepcopy(self)]

    def white_character_power_move_pink(self):
        #print('white_character_power_move_pink:')
        return [copy.deepcopy(self)]

    def white_character_power_move_black(self):
        #print('white_character_power_move_black:')
        return [copy.deepcopy(self)]

    def white_character_power_move_red(self):
        #print('white_character_power_move_red:')
        return [copy.deepcopy(self)]
