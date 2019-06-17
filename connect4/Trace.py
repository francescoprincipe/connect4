import config as cfg

class Trace(object):

    START = """((0, 0, 0, 0, 0, 0, 0), 
                (0, 0, 0, 0, 0, 0, 0), 
                (0, 0, 0, 0, 0, 0, 0), 
                (0, 0, 0, 0, 0, 0, 0), 
                (0, 0, 0, 0, 0, 0, 0), 
                (0, 0, 0, 0, 0, 0, 0))"""


    FIRST_MOVE = True

    def __init__(self, agent_yellow, agent_red):
        if cfg.CONNECT_MODE == 3:
            self.start_yellow_state = """((0, 0, 0, 0, 0), 
                                          (0, 0, 0, 0, 0), 
                                          (0, 0, 0, 0, 0), 
                                          (0, 0, 0, 0, 0))"""

            
        if cfg.CONNECT_MODE == 4:
            self.start_yellow_state = Trace.START

        if cfg.CONNECT_MODE == 2:
           self.start_yellow_state = """((0, 0, 0, 0), 
                                         (0, 0, 0, 0))"""
           
        self.start_red_state = None
        self.result_yellow_state = None
        self.result_red_state = None
        self.agent_yellow = agent_yellow
        self.agent_red = agent_red
        self.last_action_red = None
        self.last_action_yellow = 2
        self.last_possible_actions_red = None
        self.last_possible_actions_yellow = None

    def learn(self, agent, prev_state, result_state, reward, board, actions, chosen_action):

        maxQnew = None

        # Update current state
        prev = agent.getQ(prev_state, chosen_action)

        if maxQnew == None:
            maxQnew = max([agent.getQ(result_state, a) for a in actions])
        updating = prev + cfg.ALPHA * ((reward + cfg.GAMMA*maxQnew) - prev)

        # Update learning table
        if agent == self.agent_yellow:
            agent.reset_qs()
            count=0
            while count < cfg.BOARD_SIZE[1]:
                agent.append_to_qs(agent.getQ(prev_state, count))
                count+=1

        # Learning!
        agent.update_Q(actions, prev_state, chosen_action, updating)

        # Prova
        #if cfg.CONNECT_MODE == 4:
        #    if reward == cfg.WON: # Prova
        #        for i in actions: # Prova
        #            if i != chosen_action: # Prova
        #                prev = agent.getQ(prev_state, i) # Prova
        #                updating = prev + cfg.ALPHA * (cfg.LOST - prev) # Prova
        #                agent.update_Q(actions, prev_state, i, updating) # Prova

    def new_game(self):
        Trace.FIRST_MOVE = True
        self.start_yellow_state = Trace.START
        self.start_red_state = None
        self.result_yellow_state = None
        self.result_red_state = None
        self.last_action_red = None
        self.last_action_yellow = 2
        self.last_possible_actions_yellow = None
        self.last_possible_actions_red = None

    def learning_yellow(self, board, actions, chosen_action, game_over, game_logic):
        self.last_action_red = chosen_action
        self.last_possible_actions_red = actions

        if Trace.FIRST_MOVE==True:
            return
        reward_yellow = cfg.MOVE
        if game_logic.check_game_over() == True:
            if game_logic.get_winner() == 0:
                reward_red = cfg.TIE
                reward_yellow = cfg.TIE
            elif game_logic.get_winner()==2:
                #print("HA VINTO ROSSO")
                reward_red = cfg.WON
                reward_yellow = cfg.LOST
            else:
                print("ERRORE, non dovrebbe finire qui")
                exit(0)
            self.learn(self.agent_yellow, self.start_yellow_state, self.result_yellow_state, reward_yellow, board, self.last_possible_actions_yellow, self.last_action_yellow)
            self.result_red_state = self.result_yellow_state # non ci sono altre mosse dopo
            self.learn(self.agent_red, self.start_red_state, self.result_red_state, reward_red, board, actions, chosen_action)
            self.new_game()
        else:
            self.learn(self.agent_yellow, self.start_yellow_state, self.result_yellow_state, reward_yellow, board, self.last_possible_actions_yellow, self.last_action_yellow)
            self.start_yellow_state = self.result_yellow_state
            self.result_yellow_state = None
            

    def learning_red(self, board, actions, chosen_action, game_over, game_logic):
        self.last_action_yellow = chosen_action
        self.last_possible_actions_yellow = actions

        if Trace.FIRST_MOVE==True:
            Trace.FIRST_MOVE = False
            return

        reward_red = cfg.MOVE
        if game_logic.check_game_over() == True:
            if game_logic.get_winner() == 0:
                reward_red = cfg.TIE
                reward_yellow = cfg.TIE
            elif game_logic.get_winner()==1:
                #print("HA VINTO GIALLO")
                reward_red = cfg.LOST
                reward_yellow = cfg.WON
            else:
                print("ERRORE, non dovrebbe finire qui")
                exit(0)
            self.learn(self.agent_red, self.start_red_state, self.result_red_state, reward_red, board, self.last_possible_actions_red, self.last_action_red)
            self.result_yellow_state = self.result_red_state # non ci sono altre mosse dopo
            self.learn(self.agent_yellow, self.start_yellow_state, self.result_yellow_state, reward_yellow, board, actions, chosen_action)
            self.new_game()
        else:
            self.learn(self.agent_red, self.start_red_state, self.result_red_state, reward_red, board, self.last_possible_actions_red, self.last_action_red)
            self.start_red_state = self.result_red_state
            self.result_red_state = None

    def set_start_yellow_state(self, state):
        self.start_yellow_state = state

    def set_start_red_state(self, state):
        self.start_red_state = state

    def set_result_yellow_state(self, state):
        self.result_yellow_state = state

    def set_result_red_state(self, state):
        if Trace.FIRST_MOVE == False:
            self.result_red_state = state
        else:
            self.start_red_state = state

    def get_start_yellow_state(self):
        return self.start_yellow_state

    def get_start_red_state(self):
        return self.start_red_state
    def get_result_yellow_state(self):
        return self.result_yellow_state
    def get_result_red_state(self):
        return self.result_red_state
