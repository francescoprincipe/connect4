import pygame
import config as cfg
import imp
import Board
import Slot
import GameLogic as gl
import Options as opt
import HumanPlayer as hp
import AgentPlayer as ap
import Coin
import ColumnFullException as exception
import Trace
import Menu
import GameOver
import sys
import os
import Options

class GameView(object):
    # A class that represents the displays in the game

    ## Constructor
    def __init__(self, width=cfg.WINDOW_WIDTH, height=cfg.WINDOW_HEIGHT):

        #Initialize pygame, window, background, font,...
        pygame.init()
        pygame.mixer.init()

        # Store a copy of setting parameters
        self.epsilon = cfg.EPSILON
        self.games_number = cfg.GAMES_NUMBER
        self.speed_train = cfg.SPEED_TRAIN
        self.music = cfg.MUSIC
        self.connect_mode = cfg.CONNECT_MODE

        self.game_logic = None

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()

        self.menu = Menu.Menu(self.background, width, height, self.connect_mode)
        self.options = Options.Options(self.background, width)
        self.game = GameOver.GameOver(self.background, width)

        self.win_list = [0,0,0]

    def initialize_game_variables(self, game_mode):
        # Initialize the game board and the GameLogic object

        # Who is yellow? Who red?
        colour_p1 = 2
        colour_p2 = 1

        if game_mode == "TeachAgents" or game_mode=="Singleplayer":

            # Player 1
            self.p1 = hp.HumanPlayer(colour_p1)

            self.p2 = ap.AgentPlayer(colour_p2, "qlearner", self.connect_mode, game_mode)
            self.p1.set_opponent(self.p2)

            self.trace = Trace.Trace(self.p2, self.p1)
            self.p1.set_trace(self.trace)
            self.p2.set_trace(self.trace)

        elif game_mode == "Multiplayer":
            self.p1 = hp.HumanPlayer(colour_p1)
            self.p2 = hp.HumanPlayer(colour_p2)

        elif game_mode == "Options":
            pass

        elif game_mode == "AgentsLearn":
            self.p1 = ap.AgentPlayer(colour_p1, "qlearner", self.connect_mode, "AgentsLearn")
            self.p2 = ap.AgentPlayer(colour_p2, "qlearner", self.connect_mode, "AgentsLearn")
            self.trace = Trace.Trace(self.p2, self.p1)
            self.p1.set_trace(self.trace)
            self.p2.set_trace(self.trace)
            self.p1.set_opponent(self.p2)
            self.p2.set_opponent(self.p1)


        self.game_board = Board.Board(cfg.BOARD_SIZE[0], cfg.BOARD_SIZE[1], game_mode)
        (self.board_rows, self.board_cols) = self.game_board.get_dimensions()
        self.game_logic = gl.GameLogic(self.game_board, self.connect_mode)

    def main_menu(self, gameNumber=None):
        if gameNumber == None:
            gameNumber = self.games_number
        # Display the main menu screen
        self.menu.set_menu_mode(True)
        play_game = False
        self.options.set_options_mode(False)
        self.background.fill(cfg.LIGHT_BLUE)
        self.menu.draw_menu()

        if cfg.MUSIC==True:
            pygame.mixer.music.load('music1.mp3')
            pygame.mixer.music.play(-1)
        if cfg.MUSIC == False:
            pygame.mixer.music.stop()

        while self.menu.get_menu_mode():
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    play_game, game_mode = self.menu.onClick(position, play_game, self.options, None)

                if event.type == pygame.KEYDOWN:
                    self.connect_mode = self.menu.onPress(event.key, self.options)

                if event.type == pygame.QUIT:
                    self.menu.set_menu_mode(False)
                    self.options.set_options_mode(False)
                    pygame.quit()
                    sys.exit(0)

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        if not (play_game or self.options.get_options_mode()):
            pygame.quit()
            sys.exit(0)

        elif game_mode == "AgentsLearn" or game_mode == "TeachAgents":
            self.run(game_mode, gameNumber)

        else:
            self.run(game_mode, 1)


    def run(self, game_mode, gameNumber=1000000):
        # Main loop in the game

        if game_mode !='Options':
            self.initialize_game_variables(game_mode)
            while (gameNumber > 0):
                self.game_board = Board.Board(cfg.BOARD_SIZE[0], cfg.BOARD_SIZE[1],game_mode)
                (self.board_rows, self.board_cols) = self.game_board.get_dimensions()
                self.game_logic = gl.GameLogic(self.game_board, self.connect_mode)
                self.background.fill(cfg.BLACK)
                self.game_board.draw(self.background, game_mode)
                self.game.set_game_over(False)
                turn_ended = False
                uninitialized = True
                current_type = 1

                if game_mode == "TeachAgents" or game_mode == "Singleplayer":
                    human_turn = (self.p1.get_coin_type() == current_type)

                elif game_mode == "Multiplayer":
                    human_turn = True

                elif game_mode == "Options":
                    pass

                elif game_mode == "AgentsLearn":
                    human_turn = False

                p1_turn = (self.p1.get_coin_type() == current_type)

                (first_slot_X, first_slot_Y) = self.game_board.get_slot(0,0).get_position()
                coin = Coin.Coin(current_type)
                self.game.set_game_over_screen(False)
                while not self.game.get_game_over():

                    if uninitialized:
                        coin = Coin.Coin(current_type)
                        coin.set_position(first_slot_X, first_slot_Y - Slot.Slot.SIZE)
                        coin.set_column(0)
                        uninitialized = False
                        coin_inserted = False

                    coin.draw(self.background, False)

                    current_player = self.p1 if p1_turn else self.p2

                    if not human_turn:
                        temp = current_player.complete_move(coin, self.game_board, self.game_logic, self.background)
                        self.game.set_game_over(temp)
                        coin_inserted = True
                        uninitialized = True

                    # handle the keyboard events
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            position = pygame.mouse.get_pos()
                            clicked = self.game_board.onClick(position, self.menu, self.game)
                            if game_mode == "AgentsLearn" or game_mode == "TeachAgents":
                                #execfile( "main.py", {'GAMES_NUMBER':5000})
                                #os.system('python main.py 50000')
                                #os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) #return
                                if clicked:
                                    os.execv(sys.executable, ['python'] + sys.argv)
                        if event.type == pygame.QUIT:
                            self.game.set_game_over(True)
                            return
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                exit()
                            if event.key == pygame.K_RIGHT and human_turn:
                                if (coin.get_column() + 1 < self.board_cols):
                                    coin.move_right(self.background)

                            elif event.key == pygame.K_LEFT and human_turn:
                                if (coin.get_column() - 1 >= 0):
                                    coin.move_left(self.background)

                            elif event.key == pygame.K_RETURN and human_turn and not coin_inserted:
                                try:
                                    temp = self.game_board.insert_coin(coin, self.background, self.game_logic)
                                    self.game.set_game_over(temp)
                                    last_action_human = coin.col
                                    if not game_mode == "Multiplayer":
                                        current_player.complete_move(self.game_board, last_action_human, self.game_logic)
                                    uninitialized = True
                                    coin_inserted = True

                                except exception.ColumnFullException as e:
                                    pass

                    if self.game.get_game_over():
                        winner = self.game_logic.determine_winner_name()

                        if winner!="STOP":
                            winner_value = self.game_logic.get_winner()
                            if (game_mode == "AgentsLearn" or game_mode=="TeachAgents"):
                                self.win_list[winner_value]+=1
                            self.game.set_game_over_screen(True)
                        pygame.display.set_caption(str("Connect 4 : yellow {}, tie {}, red {}").format(self.win_list[1], self.win_list[0], self.win_list[2]))



                    if coin_inserted:
                        if game_mode == "TeachAgents" or game_mode=="Singleplayer":
                            human_turn = not human_turn
                        current_type = 1 if current_type == 2 else 2
                        p1_turn = not p1_turn



                    pygame.display.flip()
                    self.screen.blit(self.background, (0, 0))

                gameNumber -= 1

            if game_mode == "AgentsLearn" :
                self.main_menu()

            else:
                if winner!="STOP":
                    self.game.game_over(winner, self.menu, self.screen)
                self.main_menu()

        else:
             # Display the game over screen
            self.options.set_options_mode(True)
            self.menu.set_menu_mode(False)
            self.background.fill(cfg.LIGHT_BLUE)
            self.options.draw_options(self.games_number, self.speed_train, self.music, self.epsilon)


            self.games_number, self.speed_train, self.music, self.epsilon = self.options.running_options(self.games_number, self.speed_train, self.music, self.epsilon, self.screen, self.menu)
            self.main_menu()
