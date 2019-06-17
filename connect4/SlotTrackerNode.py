class SlotTrackerNode():
    """A class that that represents the node in the internal graph
    representation of the game board"""

    def __init__(self):
        """
        Initialize the SlotTrackerNode with pointers to Nodes in all
        8 directions surrounding along with a score count in each direction
        """
        self.top_left = None
        self.top_right = None
        self.top = None
        self.left = None
        self.right = None
        self.bottom_left = None
        self.bottom = None
        self.bottom_right = None
        self.top_left_score = 1
        self.top_right_score = 1
        self.top_score = 1
        self.left_score = 1
        self.right_score = 1
        self.bottom_left_score = 1
        self.bottom_score = 1
        self.bottom_right_score = 1
        self.value = 0
        self.visited = False
