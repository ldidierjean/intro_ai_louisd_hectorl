from os import name
import sys
import wandb
from Game import Game
from Player import Player
import model
from datetime import datetime
import threading

if __name__ == '__main__':
    # 1. Start a W&B run
    wandb.init(project='AI', name='Training run', entity='ai_louis_hector')

    # Model training here
    fantom_agent = model.Agent(93, 10, 100, 5)
    fantom_agent.set_training(True)
    inspector_agent = model.Agent(93, 10, 100, 5)
    inspector_agent.set_training(True)

    episode = 0

    try:
        while True:
            game1 = Game(Player(0, fantom_agent), Player(1, None))
            game1.lancer()
            
            game2 = Game(Player(0, None), Player(1, inspector_agent))
            game2.lancer()

            wandb.log({
                        "Episode": episode,
                        "Fantom total reward": fantom_agent.get_total_rewards(),
                        "Fantom step": fantom_agent.get_current_step(),
                        "Fantom loss": fantom_agent.loss,
                        "Inspector total reward": inspector_agent.get_total_rewards(),
                        "Inspector step": inspector_agent.get_current_step(),
                        "Inspector loss": inspector_agent.loss
            })

            fantom_agent.reset_total_rewards()
            inspector_agent.reset_total_rewards()
            episode += 1
    except KeyboardInterrupt:
        print('Stopping training.')

    print('Saving both trained models. Please wait...')

    filepath = './saved_models/' + datetime.now().strftime("%d-%m-%Y") + 'Fantom'

    print("Saving fantom model: " + filepath)

    fantom_agent.save_weights(filepath)

    filepath = './saved_models/' + datetime.now().strftime("%d-%m-%Y") + 'Inspector'

    print("Saving inspector model: " + filepath)

    inspector_agent.save_weights(filepath)
