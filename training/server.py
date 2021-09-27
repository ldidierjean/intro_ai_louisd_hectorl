import sys
import wandb

from Game import Game
from Player import Player
from hector_src import model


"""
    The order of connexion of the sockets is important.
    inspector is player 0, it must be represented by the first socket.
    fantom is player 1, it must be representer by the second socket.
"""


if __name__ == '__main__':
    # 1. Start a W&B run
    wandb.init(project='AI', entity='lekk')

    # 2. Save model inputs and hyperparameters
    config = wandb.config
    config.learning_rate = 0.01

    # Model training here
    agent1 = model.Agent(85, 10, 10, 10)
    agent2 = model.Agent(85, 10, 10, 10)
    players = [Player(1, agent1), Player(0, agent2)]
    scores = []
    game = Game(players)
    game.lancer()

    # 3. Log metrics over time to visualize performance
    with tf.Session() as sess:
        # ...
        wandb.tensorflow.log(tf.summary.merge_all())

