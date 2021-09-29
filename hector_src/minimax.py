from hector_src.enum import PlayerType
from state_generator import generate_new_states_from_state
from enum import PlayerType
import scoring

def __is_end_state(state):
    pass

def __get_score_of_state(state, player_type: PlayerType):
    if player_type == PlayerType.FANTOM:
        return scoring.score_state_for_fantom(state)
    else:
        return scoring.score_state_for_inspector(state)

def minimax(state, depth: int, is_maximizing: bool, player_type: PlayerType):
    if depth == 0 or __is_end_state(state):
        return __get_score_of_state(state, player_type)

    new_states = generate_new_states_from_state(state)

    if is_maximizing:
        value = float('-inf')
        for new_state in new_states:
            result = minimax(new_state, depth - 1, False, player_type)
            if result > value:
                value = result
        return value
    else:
        value = float('inf')
        for new_state in new_states:
            result = minimax(new_state, depth - 1, True, player_type)
            if result < value:
                value = result
        return value