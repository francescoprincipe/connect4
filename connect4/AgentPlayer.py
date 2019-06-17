import Player as player
import RandomPlayer as randomPlaeyer
import QLearningPlayer as qlearningPlayer
import Table

class AgentPlayer(player.Player):
    # A class that represents an AI player in the game

    def give_opponent_your_state(self):
        return self.player.give_opponent_your_state()

    def take_opponent_state(self, state):
        self.player.take_opponent_state(state)

    ## -- Setter --
    def set_opponent(self, opponent):
        self.player.set_opponent(opponent)

    def set_trace(self, trace):
        self.player.set_trace(trace)

    def get_qs(self):
        return self.player.get_qs()

    def append_to_qs(self, item):
        self.player.append_to_qs(item)

    def reset_qs(self):
        self.player.reset_qs()

    def getQ(self, state, action):
        return self.player.getQ(state, action)

    def update_Q(self, actions, prev_state, chosen_action, updating):
        self.player.update_Q(actions, prev_state, chosen_action, updating)

    ## -- Getter --
    def get_last_state(self):
        return self.player.get_last_state()
    def get_last_action(self):
        return self.player.get_last_action()

    def __init__(self, coin_type, player_type, sequence_length, mode, opponent=None):
        # Initialize an AI with the proper type which are one of Random and
        # Q-learner currently

        ## In fact the agent can be used both for single player mode and AgentsLearn mode
        self.mode = mode

        if player_type == "random":
            self.player = randomPlaeyer.RandomPlayer(coin_type)
        if player_type == "qlearner":
            self.player = qlearningPlayer.QLearningPlayer(coin_type, sequence_length, mode)
        else:
            self.player = qlearningPlayer.QLearningPlayer(coin_type, sequence_length, mode)

        self.last_action = None
        self.coin_type = coin_type
        self.player_type = player_type
        self.table_learning = None

    def complete_move(self, coin, board, game_logic, background):
        # Move the coin and decide which slot to drop it in and learn from the
        # chosen move

        ## Qlearner needs board state to some operations
        if self.player_type == "qlearner":# or self.player_type=="qlearner-opponent":
            self.player.set_board(board)

        actions = board.get_available_actions()
        state = board.get_state()
        chosen_action = self.choose_action(state, actions)
        self.last_action = chosen_action
        coin.move_right(background, chosen_action)
        coin.set_column(chosen_action)
        game_over = board.insert_coin(coin, background, game_logic)

        #print(self.player.get_coin_type())
        #self.give_opponent_your_state()

        if self.mode == "TeachAgents" or self.mode == "AgentsLearn":
            self.player.traceLearn(board, actions, chosen_action, game_over, game_logic)
            if self.get_coin_type() == 1:
                if self.table_learning == None:
                    self.table_learning = Table.Table(background)
                else:
                    self.table_learning.update(self.get_qs())
        return game_over

    ## Setter for mode
    def set_mode(self,mode):
        # Set the agent mode
        self.mode = mode

    ## Getter for coin_type
    def get_coin_type(self):
        # Return the coin type of the AI player
        return self.player.get_coin_type()

    def choose_action(self, state, actions):
        # Choose an action (which slot to drop in) based on the state of the board
        return self.player.choose_action(state, actions)
