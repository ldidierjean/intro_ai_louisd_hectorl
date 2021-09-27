from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
import mappings

def build_model(input_size, output_size, hidden_size, nb_hidden_layers):
    model = Sequential()
    model.add(Flatten(input_shape=(1, input_size)))
    for _ in range(nb_hidden_layers):
        model.add(Dense(hidden_size))
        model.add(Activation('relu'))
    model.add(Dense(output_size))
    model.add(Activation('linear'))
    print(model.summary())
    return model

def build_dqn_agent(input_size, output_size, hidden_size, nb_hidden_layers):
    model = build_model(input_size, output_size, hidden_size, nb_hidden_layers)

    memory = SequentialMemory(limit=100000, window_length=1)
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.01, value_test=0,
                              nb_steps=100000)
    dqn = DQNAgent(model=model, nb_actions=output_size, memory=memory, policy=policy, gamma=0.99,
               target_model_update=300)
    dqn.compile(Adam(lr=1e-5), metrics=['mae'])
    
    return dqn

def game_data_to_state(game_data):
    question_type = [0] * 22
    question_type[mappings[game_data['question type']]] = 1
    state = []
    return state

def game_data_to_fantom_state(game_data):
    state = []
    return state

class Agent():
    def __init__(self, input_size, output_size, hidden_size, nb_hidden_layers):
        model = Sequential()
        model.add(Flatten(input_shape=(1, input_size)))
        for _ in range(nb_hidden_layers):
            model.add(Dense(hidden_size))
            model.add(Activation('relu'))
        model.add(Dense(output_size))
        model.add(Activation('linear'))
        print(model.summary())

        memory = SequentialMemory(limit=100000, window_length=10)
        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.01, value_test=0,
                              nb_steps=100000)
        self.__dqn = DQNAgent(model=model, nb_actions=output_size, memory=memory, policy=policy, gamma=0.99,
               target_model_update=300)
        self.__dqn.compile(Adam(lr=1e-5), metrics=['mae'])
    
    def get_action(self, game_data):
        state = game_data_to_state(game_data)
        nb_possible_actions = len(game_data['data'])

        action_index = self.__dqn.forward(state)

        if action_index >= nb_possible_actions:
            action_index = nb_possible_actions - 1
        return action_index

    def give_reward(self, reward, is_terminal):
        self.__dqn.backward(reward, is_terminal)
    
    def set_training(self, training):
        self.__dqn.training = training
