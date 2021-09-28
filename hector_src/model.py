from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam
import numpy
import tensorflow as tf
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
import mappings

def game_data_to_state(game_data):
    question_type = [0] * 22
    question_type[mappings.question_mappings[game_data['question type']]] = 1

    data = [0] * 10
    if isinstance(game_data['data'][0], int):
        for i in range(len(game_data['data'])):
            data[i] = game_data['data'][i]
    elif isinstance(game_data['data'][0], str):
        for i in range(len(game_data['data'])):
            data[i] = mappings.color_mappings[game_data['data'][i]]
    else:
        for i in range(len(game_data['data'])):
            data[i] = mappings.color_mappings[game_data['data'][i]['color']]
        

    carlotta = game_data['game state']['exit'] - game_data['game state']['position_carlotta']
    tour = game_data['game state']['num_tour']
    shadow = game_data['game state']['shadow']
    blocked = [game_data['game state']['blocked'][0], game_data['game state']['blocked'][1]]
    game_state = [carlotta, tour, shadow] + blocked
    
    characters = [0] * (8 * 3)

    for character in game_data['game state']['characters']:
        offset = mappings.color_mappings[character['color']]
        characters[offset] = 1 if character['suspect'] else 0
        characters[offset + 1] = character['position']
        characters[offset + 2] = 1 if character['power'] else 0
    
    active = [0] * 8

    for active_character in game_data['game state']['active character_cards']:
        active[mappings.color_mappings[active_character['color']]] = 1

    fantom = [0] * 8

    if 'fantom' in game_data['game state']:
        fantom[mappings.color_mappings[game_data['game state']['fantom']]] = 1

    state = question_type + data + game_state + characters + active + fantom
    return state

class Agent():
    def __init__(self, input_size, output_size, hidden_size, nb_hidden_layers):
        model = Sequential()
        model.add(Flatten(input_shape=(1, input_size)))
        model.add(Dense(hidden_size))
        model.add(Activation('relu'))
        model.add(Dense(hidden_size))
        model.add(Activation('relu'))
        model.add(Dense(hidden_size))
        model.add(Activation('relu'))
        model.add(Dense(hidden_size))
        model.add(Activation('relu'))
        model.add(Dense(hidden_size))
        model.add(Activation('relu'))
        model.add(Dense(hidden_size))
        model.add(Activation('relu'))
        model.add(Dense(output_size))
        model.add(Activation('linear'))
        print(model.summary())

        memory = SequentialMemory(limit=100000, window_length=1)
        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.01, value_test=0,
                              nb_steps=100000)
        self.__dqn = DQNAgent(model=model, nb_actions=output_size, memory=memory, policy=policy, gamma=0.99,
               target_model_update=200)
        self.__dqn.compile(Adam(lr=1e-4), metrics=['mae'])

        self.__dqn.training = True

        self.total_rewards = 0

        self.current_accumulated_rewards = 0
    
    def get_action(self, game_data):
        state = game_data_to_state(game_data)
        nb_possible_actions = len(game_data['data'])

        action_index = self.__dqn.forward(state)

        self.__dqn.step += 1

        if action_index >= nb_possible_actions:
            action_index = nb_possible_actions - 1
        return action_index
    
    def accumulate_reward(self, add):
        self.current_accumulated_rewards += add
    
    def release_accumulated_rewards(self, terminal):
        self.__dqn.backward(self.current_accumulated_rewards, terminal)
        self.total_rewards += self.current_accumulated_rewards
        self.current_accumulated_rewards = 0

    def give_reward(self, reward, is_terminal):
        self.total_rewards += reward
        self.__dqn.backward(reward, is_terminal)

    def get_total_rewards(self):
        return self.total_rewards
    
    def reset_total_rewards(self):
        self.total_rewards = 0
    
    def set_training(self, training):
        self.__dqn.training = training
    
    def save_weights(self, filepath):
        self.__dqn.save_weights(filepath)

    def get_current_step(self):
        return self.__dqn.step
