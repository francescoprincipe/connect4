import config as cfg
import Player as player
import pygame
import random
import DBHelper as db
import Trace

class QLearningPlayer(player.Player):
    #A class that represents an AI using Q-learning algorithm

    def __init__(self, coin_type, sequence_length, mode, opponent=None, epsilon=cfg.EPSILON, alpha=cfg.ALPHA, gamma=cfg.GAMMA):

        player.Player.__init__(self, coin_type)

        # The agent plays yellow coin or thinks to play with yellow coins
        self.coin_type = coin_type
        if coin_type != 1:
            self.inverted = True
        else:
            self.inverted = False

        # The agent, if winner, rewards the loser opponent
        self.opponent = opponent
        # Otherwise, the opponent, rewards it
        self.last_action = None
        self.last_state = None

        # It can be 2, 3, 4
        self.sequence_length = sequence_length

        if mode != "TeachAgents" and mode!="AgentsLearn":
            self.epsilon = 0
        else:
            self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha   = alpha   # learning rate
        self.gamma   = gamma   # discount factor for future rewards

        self.board   = None    # board
        self.Qs = []           # previous Qs
        self.db = db.DBHelper("connect{}Qs".format(self.sequence_length),"connect{}.db".format(self.sequence_length))

        self.opponent_state = None
        self.trace = None

    def set_trace(self, trace):
        self.trace = trace

    ## Given a state and an action, search in the db the associated Q
    def getQ(self, state, action):
        # Given a state and an action, search in the db the associated Q

        # If state isn't stored
        if self.db.exists_state(state) == False:

            # It may be a specular state stored, so try search it in the db

            # If specular state isn't stored, it's okay, set Q as default value
            str_specular_state = str(tuple(tuple(x)[::-1] for x in self.string_to_tuple(str(state))))
            if self.db.exists_state(str_specular_state) == False:
                Q = 0.0

            # If specular state is stored, great, set Q as the values of that state-action
            else:
                Qs = self.db.get_qs(str_specular_state)
                specular_action = cfg.BOARD_SIZE[1]-1-action
                Q = Qs[specular_action]

        # If state is stored
        else:
            Qs = self.db.get_qs(state)
            Q = Qs[action]

        return Q

    # Return an action based on the best move recommendation by the current Q-Table with a epsilon chance of
    # trying out a new move
    def choose_action(self, state, actions):

        # Add a dalay from configuration file
        pygame.time.delay(100*(20-cfg.SPEED_TRAIN))

        # The agent plays yellow coin or thinks to play with yellow coins
        if self.inverted:
            current_state = self.board.get_inverted_state(state)
        else:
            current_state = state

        #inizia sempre centrale
        if str(state)=="((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))":
            return 2
        if str(state)=="((0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0))":
            return 3

        #print(current_state)

        # Epsilon-Greedy
        if random.random() < self.epsilon: # explore!
            chosen_action = random.choice(actions)
            return chosen_action

        Qs = [self.getQ(current_state, a) for a in actions]
        maxQ = max(Qs)

        # If there are more than 1 best option; choose among them randomly
        if Qs.count(maxQ) > 1:
            best_options = [i for i in range(len(actions)) if Qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = Qs.index(maxQ)

        #print(state)

        return actions[i]

    def get_qs(self):
        return self.Qs

    def append_to_qs(self,item):
        self.Qs.append(item)

    def reset_qs(self):
        self.Qs=[]

    def give_opponent_your_state(self):
        self.opponent.take_opponent_state(str(self.board.get_prev_state()))
        #print(str(self.board.get_prev_state()))

    def take_opponent_state(self, state):
        self.opponent_state = state

    # Determine the reward based on its current state and chosen action, updates the Q table using
    # the reward recieved and the maximum future reward based on the resulting state due to the chosen action.
    def traceLearn(self, board, actions, chosen_action, game_over, game_logic):

        # The agent plays yellow coin or thinks to play with yellow coins
        if self.inverted: #AGENTE ROSSO
            #print("ROSSO_PARTENZA")
            #print(str(board.get_inverted_state(board.get_prev_state())))
            self.trace.set_start_red_state(str(board.get_inverted_state(board.get_prev_state())))
            #print("GIALLO_RESULT")
            #print(str(board.get_state()))
            self.trace.set_result_yellow_state(str(board.get_state()))
            self.trace.learning_yellow(board, actions, chosen_action, game_over, game_logic)
        else: #AGENTE GIALLO
            #print("GIALLO_PARTENZA")
            #print(str(board.get_prev_state()))
            self.trace.set_start_yellow_state(str(board.get_prev_state()))
            self.trace.set_result_red_state(str(board.get_inverted_state(board.get_state())))
            #print("ROSSO RESULT")
            #print(str(board.get_inverted_state(board.get_state())))
            self.trace.learning_red(board, actions, chosen_action, game_over, game_logic)

        if game_logic.check_game_over():
            return True
        
    def negative_reward(self):
        # Single mode -- Human call this function
        if self.opponent == None:
            self.opponent = self

        reward = -cfg.WON
        prev_state = self.opponent.get_last_state()
        chosen_action = self.opponent.get_last_action()
        prev = self.getQ(prev_state, chosen_action)
        #print(prev_state)
        maxQnew = 0.0 # TERMINAL STATE
        updating = prev + self.alpha * ((reward + self.gamma*maxQnew) - prev)
        self.update_Q([chosen_action], prev_state, chosen_action, updating)

    def string_to_tuple(self, state):
        a = []
        b = []
        for i in state:
            if i == ")":
                if a!=[]:
                    b.append(a)
                    a = []
            if i == "1" or i == "2" or i == "0":
                a.append(int(i))
        result = tuple(tuple(x) for x in b)
        return result

    # This function update Q in db
    def update_Q(self, actions, state, chosen_action, Q ):

                # Create string state
        str_state = str(state)

        str_Qs="["

        action = 0
        while action < cfg.BOARD_SIZE[1]:
            if action in actions:
                if action == chosen_action:
                    str_Qs+=str(Q)
                else:
                    str_Qs+=str(self.getQ(state,action))
            else:
                str_Qs+=str(0) # ILLEGAL ACTION
                #print(str_state)
                #print(str_q)
            action+=1
            if action<cfg.BOARD_SIZE[1]:
                str_Qs+=","
            else:
                str_Qs+="]"


        str_specular_Qs="["
        self.string_to_tuple(state)
        str_specular_state = str(tuple(tuple(x)[::-1] for x in self.string_to_tuple(state)))

        actions_specular = []
        for a in actions:
            actions_specular.append(cfg.BOARD_SIZE[1]-1-a)
        actions_specular = actions_specular[::-1]

        action = 0
        while action < cfg.BOARD_SIZE[1]: # Per ogni colonna
            if action in actions_specular: # se l'azione e disponibile
                if action == cfg.BOARD_SIZE[1]-1-chosen_action: # se l'azione disponibile e quella scelta
                    str_specular_Qs+=str(Q)
                else:
                    #print(self.getQ(state, cfg.BOARD_SIZE[1]-1-action))
                    str_specular_Qs+=str(self.getQ(state, cfg.BOARD_SIZE[1]-1-action)) #getQ si aspetta uno stato non speculare
            else:
                str_specular_Qs+=str(0) # ILLEGAL ACTION
                #print(str_state)
                #print(str_q)
            action+=1
            if action<cfg.BOARD_SIZE[1]:
                str_specular_Qs+=","
            else:
                str_specular_Qs+="]"

        # If the state isn't stored
        if self.db.update_row(str_state, str_Qs) == False:

            # It may be a specular state stored, so try update it in table Qs

            # If the specular state isn't stored
            if self.db.update_row(str_specular_state, str_specular_Qs)==False:

                # Add new state
                if str_state == "((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0))":
                    str_Qs = "[0,0,100,0,0]" #Consiglio d'amico

                self.db.insert_row(str_state, str_Qs)

        # If state is stored
        #else: do nothing

        #exit()

    # ---- Getter ----
    # Return the coin type of the AI player
    def get_coin_type(self):
        return self.coin_type

    # Return the last state before the last agent action
    def get_last_state(self):
        return self.last_state

    # Return the last action choose by the agent
    def get_last_action(self):
        return self.last_action


    # -- Setter --
    # Set the opponent of the AI player
    def set_opponent(self, opponent):
        self.opponent=opponent

    # Set an object board for the agent
    def set_board(self, board):
        self.board = board
