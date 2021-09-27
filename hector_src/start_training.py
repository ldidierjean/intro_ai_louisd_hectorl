import sys
import wandb

from Game import Game
from Player import Player
import model


"""
    The order of connexion of the sockets is important.
    inspector is player 0, it must be represented by the first socket.
    fantom is player 1, it must be representer by the second socket.
"""


if __name__ == '__main__':
    # 1. Start a W&B run
    #wandb.init(project='AI')

    # 2. Save model inputs and hyperparameters
    config = wandb.config
    config.learning_rate = 0.01

    # Model training here
    agent1 = model.Agent(85, 10, 100, 8)
    agent1.set_training(True)
    agent2 = model.Agent(85, 10, 100, 8)
    agent2.set_training(True)

    episode = 0

    try:
        while True:
            game = Game(Player(0, agent1), Player(1, agent2))
            game.lancer()
            """
            wandb.log({
                        "Episode": episode,
                        "Inspector total reward": agent1.get_total_rewards(),
                        "Fantom total reward": agent2.get_total_rewards()
            })
            """
            agent1.reset_total_rewards()
            agent2.reset_total_rewards()
            episode += 1
    except KeyboardInterrupt:
        print('\nStopping training.')