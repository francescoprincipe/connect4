class Player():
    # A class that represents a player in the game"""

    ## Constructor
    def __init__(self, coin_type):
        # Initialize a player with their coin type

        self.coin_type = coin_type

    def complete_move(self):
        # A method to make a move and update any learning parameters if any
        pass

    ## -- Getter --
    def get_coin_type(self):
        # Return the coin type of the player
        return self.coin_type

    ## -- Setter --
    def set_coin_type(self, coin_type):
        # Set the coin type of a player
        self.coin_type = coin_type

    ## -- Converter --
    # String colour to code colour
    def _get_code_colour(self, coin_type):
        if coin_type == "YELLOW":
            return 1
        elif coin_type == "RED":
            return 2

    # code colour to string colour
    def _get_string_colour(self, coin_type):
        if coin_type == 1:
            return "YELLOW"
        elif coin_type == 2:
            return "RED"
