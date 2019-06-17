class GameLogic():
    # A class that handles win conditions and determines winner"""

    def set_win_sequence_length(self, connect_mode):
        self.WIN_SEQUENCE_LENGTH = connect_mode
    def get_win_sequence_length(self):
        return self.WIN_SEQUENCE_LENGTH

    def __init__(self, board, connect_mode=4):
        # Initialize the GameLogic object with a reference to the game board

        self.WIN_SEQUENCE_LENGTH = connect_mode

        self.board = board
        (num_rows, num_columns) = self.board.get_dimensions()
        self.board_rows = num_rows
        self.board_cols = num_columns
        self.winner_value = 0

    def check_game_over(self):
        # Check whether the game is over which can be because of a tie or one
        # of two players have won

        (last_visited_nodes, player_value) = self.board.get_last_filled_information()
        representation = self.board.get_representation()
        player_won = self.search_win(last_visited_nodes, representation)

        if player_won:
            self.winner_value = player_value

        return ( player_won or self.board.check_board_filled() )

    def search_win(self, last_visited_nodes, representation):
        # Determine whether one of the players have won

        for indices in last_visited_nodes:
            current_node = representation[indices[0]][indices[1]]
            if ( current_node.top_left_score == self.WIN_SEQUENCE_LENGTH or
                 current_node.top_score == self.WIN_SEQUENCE_LENGTH or
                 current_node.top_right_score == self.WIN_SEQUENCE_LENGTH or
                 current_node.left_score == self.WIN_SEQUENCE_LENGTH or
                 current_node.right_score == self.WIN_SEQUENCE_LENGTH or
                 current_node.bottom_left_score == self.WIN_SEQUENCE_LENGTH or
                 current_node.bottom_score == self.WIN_SEQUENCE_LENGTH or
                 current_node.bottom_right_score == self.WIN_SEQUENCE_LENGTH ):
                return True

        return False

    def search_possible_win(self, last_visited_nodes, representation):
        # Determine whether one of the players have won

        for indices in last_visited_nodes:
            current_node = representation[indices[0]][indices[1]]
            if ( current_node.top_left_score == self.WIN_SEQUENCE_LENGTH-1 or
                 current_node.top_score == self.WIN_SEQUENCE_LENGTH-1 or
                 current_node.top_right_score == self.WIN_SEQUENCE_LENGTH-1 or
                 current_node.left_score == self.WIN_SEQUENCE_LENGTH-1 or
                 current_node.right_score == self.WIN_SEQUENCE_LENGTH-1 or
                 current_node.bottom_left_score == self.WIN_SEQUENCE_LENGTH-1 or
                 current_node.bottom_score == self.WIN_SEQUENCE_LENGTH-1 or
                 current_node.bottom_right_score == self.WIN_SEQUENCE_LENGTH-1 ):
                return True

        return False

    def check_game_about_over(self):
        # Check whether the game is over which can be because of a tie or one
        # of two players have won

        (last_visited_nodes, player_value) = self.board.get_last_filled_information()
        representation = self.board.get_representation()
        player_won = self.search_possible_win(last_visited_nodes, representation)

        if player_won:
            self.winner_value = player_value

        return ( player_won or self.board.check_board_filled() )

    def determine_winner_name(self):
        # Return the winner's name

        if (self.winner_value == 1):
            return "YELLOW"
        elif (self.winner_value == 2):
            return "RED"
        elif self.board.check_board_filled():
            return "TIE"
        else:
            return "STOP"

    def get_winner(self):
        # Return the winner coin type value

        return self.winner_value




# Se ho due pedine vicine devo cercare di completarle
# Se l'avversario ha due pedine vicine devo fermarlo ma se le ho anche io devo vincere
# se l'avversario ha una pedina con due spazi a dx e due spazi a sx devo mettere pedina o a sx
# o a dx, se la metto sopra, vince sicuramente-
# se ha perso do reward negativo ad ultima azione
