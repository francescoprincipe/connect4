import Player as player

class HumanPlayer(player.Player):
    # A class that represents a human player in the game

    def __init__(self, coin_type, opponent=False):
        # Initialize a human player with their coin type
        player.Player.__init__(self, coin_type)
        self.opponent = opponent
        self.coin_type = coin_type
        self.trace = None
        

    # -- Setter --
    def set_opponent(self, opponent):
        self.opponent=opponent

    #def give_opponent_your_state(self):
    #    return self.player.give_opponent_your_state()

    #def take_opponent_state(self, state):
    #    self.player.take_opponent_state(state)

    def set_trace(self, trace):
        self.trace = trace

    def get_qs(self):
        pass

    def append_to_qs(self, item):
        pass

    def reset_qs(self):
        pass

    def getQ(self, state, action):
        return self.opponent.getQ(state, action)

    def update_Q(self, actions, prev_state, chosen_action, updating):
        self.opponent.update_Q(actions, prev_state, chosen_action, updating)

    def complete_move(self, board, chosen_action, game_logic):
        self.trace.set_start_red_state(str(board.get_inverted_state(board.get_prev_state())))
        #print("GIALLO_RESULT")
        #print(str(board.get_state()))
        self.trace.set_result_yellow_state(str(board.get_state()))
        self.trace.learning_yellow(board, board.get_available_actions(), chosen_action, None, game_logic) #GameOver none non dovrebbe servire
