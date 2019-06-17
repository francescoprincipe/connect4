import pygame
import config as cfg

class Slot():
    # A class that represents a single slot on the board
    SIZE=cfg.SPACE_SIZE

    def __init__(self, row_index, col_index, width, height, x1, y1):
        # Initialize a slot in a given position on the board
        self.BOARDIMG = pygame.image.load('board.png')
        self.BOARDIMG = pygame.transform.smoothscale(self.BOARDIMG, (cfg.SPACE_SIZE, cfg.SPACE_SIZE))

        self.content = 0
        self.row_index = row_index
        self.col_index = col_index
        self.width = width
        self.height = height
        #sfondo bianco, scommenta anche in draw
        #self.surface = pygame.Surface((width*2, height*2))
        self.x_pos = x1
        self.y_pos = y1

    def get_location(self):
        # Return the location of the slot on the game board
        return (self.row_index, self.col_index)

    def get_position(self):
        # Return the x and y positions of the top left corner of the slot on
        # the screen
        return (self.x_pos, self.y_pos)

    def set_coin(self, coin):
        # Set a coin in the slot, which can be one of two colors
        self.content = coin.get_coin_type()

    def check_slot_fill(self):
        # Return true iff a coin is placed in the slot
        return (self.content != 0)

    def get_content(self):
        # Return what is stored in the slot, 0 if it is empty
        return self.content

    def draw(self, background):
        # Draws white background
        #pygame.draw.rect(self.surface, cfg.WHITE, (1,1,self.width - 2,self.height - 2))
        #self.surface = self.surface.convert()
        #background.blit(self.surface, (self.x_pos, self.y_pos))

        # draw board over the tokens
        background.blit(self.BOARDIMG, (self.x_pos, self.y_pos))
