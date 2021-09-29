from state import State
from globals import PlayerType
import scoring

"""
"""

def __is_end_state(state: State):
    return state.pos_carlotta >= state.exit or len(state.suspect) == 1

def __get_score_of_state(state: State, player_type: PlayerType):
    if player_type == PlayerType.FANTOM:
        return scoring.score_state_for_fantom(state)
    else:
        return scoring.score_state_for_inspector(state)

def minimax(state: State, depth: int, player_type: PlayerType):
    if depth == 0 or __is_end_state(state):
        return __get_score_of_state(state, player_type)

    new_states = state.generate_state()

    if player_type == state.next_player:
        # Maximizing
        value = float('-inf')
        for new_state in new_states:
            result = minimax(new_state, depth - 1, player_type)
            if result > value:
                value = result
        return value
    else:
        # Minimizing
        value = float('inf')
        for new_state in new_states:
            result = minimax(new_state, depth - 1, player_type)
            if result < value:
                value = result
        return value