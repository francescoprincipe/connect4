import Player as player
import random

class RandomPlayer(player.Player):
    # A class that represents a computer that selects random moves based on the moves available

    def __init__(self, coin_type):
        # Initialize the computer player

        player.Player.__init__(self, coin_type)

    def choose_action(self, state, actions):
        # Choose a random action based on the available actions
        return random.choice(actions)

    def learn(self, board, action, game_over, game_logic):
        # The random player does not learn from its actions
        pass
