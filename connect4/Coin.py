import pygame
import Slot
import config as cfg

class Coin():
    # A class that represents the coin pieces used in connect 4

    def __init__(self, coin_type):
        # Initialize a coin with a given coin_type
        # (integer that represents its color)
        self.REDIMG = pygame.image.load('Coin/red.png')
        self.YELLOWIMG = pygame.image.load('Coin/yellow.png')
        self.REDIMG = pygame.transform.smoothscale(self.REDIMG, (cfg.TOKEN_SIZE, cfg.TOKEN_SIZE))
        self.YELLOWIMG = pygame.transform.smoothscale(self.YELLOWIMG, (cfg.TOKEN_SIZE, cfg.TOKEN_SIZE))
        self.BOARDIMG = pygame.image.load('board.png')
        self.BOARDIMG = pygame.transform.smoothscale(self.BOARDIMG, (cfg.SPACE_SIZE, cfg.SPACE_SIZE))
        self.dropped=False



        self.coin_type = coin_type
        self.surface = pygame.Surface((Slot.Slot.SIZE - 3, Slot.Slot.SIZE - 3))
        if (self.coin_type == 1):
            self.color = cfg.YELLOW
        else:
            self.color = cfg.RED

    def move_left(self, background):
        # Move the coin to the column that is left of its current column
        self.set_column(self.col - 1)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos - Slot.Slot.SIZE, self.y_pos)
        self.draw(background,False)

    def drop(self, background, row_num):
        # Drop the coin to the bottom most possible slot in its column
        self.set_row(row_num)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos, self.y_pos + ((self.row + 1) * Slot.Slot.SIZE))
        self.surface.fill((255,255,255))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.draw(background, 1)

    def get_coin_type(self):
        # Return the coin type
        return self.coin_type

    def draw(self, background, dropped):
        # Draw the coin on the screen
        #pygame.draw.circle(self.surface, self.color, (Slot.Slot.SIZE // 2, Slot.Slot.SIZE // 2), Coin.RADIUS)
        #self.surface = self.surface.convert_alpha()

        #background.blit(self.surface, (self.x_pos, self.y_pos))
        #self.YELLOWIMG=self.YELLOWIMG.convert_alpha()
        #self.REDIMG=self.REDIMG.convert_alpha()
        if self.color==cfg.YELLOW:
            background.blit(self.YELLOWIMG, (self.x_pos, self.y_pos))
        else:
            background.blit(self.REDIMG, (self.x_pos, self.y_pos))

        if dropped==True:
            background.blit(self.BOARDIMG, (self.x_pos, self.y_pos))

            self.color = cfg.YELLOW
        else:
            self.color = cfg.RED

    def set_position(self, x1, y1):
        # Set the position of the coin on the screen
        self.x_pos = x1
        self.y_pos = y1

    def set_column(self, col):
        # Set the column on the board in which the coin belongs
        self.col = col

    def get_column(self):
        # Get the column on the board in which the coin belongs in
        return self.col

    def set_row(self, row):
        # Set the row on the board where the coin is
        self.row = row

    def get_row(self):
        # Get the row on the board in which the coin belongs
        return self.row

    def move_right(self, background, step=1):
        # Move the coin to the column that is right of its current column
        self.set_column(self.col + 1)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos + step * Slot.Slot.SIZE, self.y_pos)
        self.draw(background,0)

    def move_left(self, background):
        # Move the coin to the column that is left of its current column
        self.set_column(self.col - 1)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos - Slot.Slot.SIZE, self.y_pos)
        self.draw(background,0)

    def drop(self, background, row_num):
        # Drop the coin to the bottom most possible slot in its column
        self.set_row(row_num)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos, self.y_pos + ((self.row + 1) * Slot.Slot.SIZE))
        self.surface.fill((255,255,255))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.draw(background, True)

    def get_coin_type(self):
        # Return the coin type
        return self.coin_type

    def draw(self, background, dropped):
        # Draw the coin on the screen
        #pygame.draw.circle(self.surface, self.color, (Slot.Slot.SIZE // 2, Slot.Slot.SIZE // 2), Coin.RADIUS)
        #self.surface = self.surface.convert_alpha()

        #background.blit(self.surface, (self.x_pos, self.y_pos))
        #self.YELLOWIMG=self.YELLOWIMG.convert_alpha()
        #self.REDIMG=self.REDIMG.convert_alpha()
        if self.color==cfg.YELLOW:
            background.blit(self.YELLOWIMG, (self.x_pos, self.y_pos))
        else:
            background.blit(self.REDIMG, (self.x_pos, self.y_pos))

        if dropped==1:
            background.blit(self.BOARDIMG, (self.x_pos, self.y_pos))
