from typing import Dict, List
from hector_src.globals import PlayerType, minimax_depth_level, cm
from hector_src.state import generate_state_from_server_question, State
from hector_src.scoring import score_state_for_fantom, score_state_for_inspector

"""

"""

def __is_end_state(state: State):
    return state.pos_carlotta >= state.exit or len(state.suspect) == 1

def __get_score_of_state(state: State, player_type: PlayerType):
    if player_type == PlayerType.FANTOM:
        return score_state_for_fantom(state)
    else:
        return score_state_for_inspector(state)

def minimax(state: State, depth: int, alpha: float, beta: float, player_type: PlayerType):
    if depth <= 0 or __is_end_state(state):
        return (__get_score_of_state(state, player_type),)

    new_states: List[State] = state.generate_state()

    if player_type == state.next_player:
        # Maximizing
        value = float('-inf')
        action_value = -1
        card = -1
        for new_state in new_states:
            result = minimax(new_state, depth - 1, alpha, beta, player_type)[0]
            if result > value:
                value = result
                action_value = new_state.choose_to_reach_state
                card = new_state.ongoing_card
            if result > alpha:
                alpha = result
            if beta <= alpha:
                break
        return (value, action_value, card)
    else:
        # Minimizing
        value = float('inf')
        action_value = -1
        card = -1
        for new_state in new_states:
            result = minimax(new_state, depth - 1, alpha, beta, player_type)[0]
            if result < value:
                value = result
                action_value = new_state.choose_to_reach_state
                card = new_state.ongoing_card
            if result < beta:
                beta = result
            if beta <= alpha:
                break
        return (value, action_value, card)

def get_response_index(question: Dict, player_type: PlayerType, ongoing_card: int):
    state = generate_state_from_server_question(question, player_type, ongoing_card)
    (_, chosen_value, card) = minimax(state, minimax_depth_level, float('-inf'), float('inf'), player_type)

    response_index = 0
    data = question['data']
    if isinstance(data[0], int):
        for i in range(len(data)):
            if data[i] == chosen_value:
                response_index = i
                break
    elif isinstance(data[0], str):
        for i in range(len(data)):
            if cm[data[i]] == chosen_value:
                response_index = i
                break
    else:
        for i in range(len(data)):
            if cm[data[i]['color']] == chosen_value:
                response_index = i
                break

    return (response_index, card)
