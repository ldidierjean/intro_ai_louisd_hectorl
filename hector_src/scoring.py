from state import State

def score_state_for_inspector(state: State):
    return (8 - len(state.suspect) * 10)

def score_state_for_fantom(state: State):
    return len(state.suspect) * 10 + state.pos_carlotta * 5