import config as cfg
import pygame

class Table(object):
    # A class that represents the learning table for the current stare of when an agent has to
    # choose an action

    BORDER_SIZE = 5
    FONT_SIZE = 15
    GAME_OVER = False

    def __init__(self, background):
        self.background = background

        # Set font type
        self.font = pygame.font.SysFont('arial', Table.FONT_SIZE)

        # Set positions and size of texts
        self.left_text_x = 750
        self.left_text_y = 200
        self.right_text_x = 1000
        self.right_text_y = 200

        # Static text
        self.text = []
        count = 0
        self.text.append("Q(state, col"+str(count+1)+")")

        # Set positions and size of a cell
        cell_x = self.left_text_x - Table.FONT_SIZE * 3
        cell_y = self.left_text_y - Table.FONT_SIZE + 100
        cell_width = len(self.text[0]) * Table.FONT_SIZE
        cell_heigth = 3 * Table.FONT_SIZE

        # Boarder
        self.left_border = []
        self.right_border = []
        self.left_cell = []
        self.right_cell = []

        # Initialize border list and cell list
        while count < cfg.BOARD_SIZE[1]:

            if count!=0:
                self.text.append("Q(state, col"+str(count+1)+")")

            ## Initialize list border
            # Border left
            border_x = cell_x-Table.BORDER_SIZE
            border_y = cell_y-Table.BORDER_SIZE + count * 50
            border_width = cell_width + 2 * Table.BORDER_SIZE
            border_heigth = cell_heigth + 2 * Table.BORDER_SIZE

            temp = pygame.Rect(border_x, border_y, border_width, border_heigth)
            self.left_border.append(temp)

            # Border right
            border_x = border_x -5+ cell_width+ 2 * Table.BORDER_SIZE

            temp = pygame.Rect(border_x, border_y, border_width, border_heigth)
            self.right_border.append(temp)

            ## Initialize list cell
            # Cell left
            temp = pygame.Rect(cell_x, cell_y + count * 50, cell_width, cell_heigth)
            self.left_cell.append(temp)

            # Cell right
            cell_right_x = cell_x + cell_width + Table.BORDER_SIZE
            temp = pygame.Rect(cell_right_x, cell_y + count * 50, cell_width, cell_heigth)
            self.right_cell.append(temp)

            count+=1

        self.draw_cell()
        self.draw_static_text()

    def draw_title(self):
        # Draw title table
        LEARNING_IMG = pygame.image.load("Title/Learning-table.png")
        learning_img_x = cfg.WINDOW_WIDTH + 70
        learning_img_y = 60

        cover_rect = pygame.Rect(learning_img_x - 50, 90, 520, 580)
        pygame.draw.rect(self.background, cfg.BLACK, cover_rect, 0)
        cover_rect = pygame.Rect(learning_img_x-40, 100, 500, 560)
        pygame.draw.rect(self.background, cfg.LIGHT_BLUE1, cover_rect, 0)

        self.background.blit(LEARNING_IMG,(learning_img_x, learning_img_y))

    def draw_cell(self):
        # A function that draws cells and their borders

        count = 0
        while count < cfg.BOARD_SIZE[1]:
            # Draw boarder
            pygame.draw.rect(self.background, cfg.BLACK, self.left_border[count], 0)
            pygame.draw.rect(self.background, cfg.BLACK, self.right_border[count], 0)

            # Draw cell
            pygame.draw.rect(self.background, cfg.WHITE, self.left_cell[count], 0)
            pygame.draw.rect(self.background, cfg.WHITE, self.right_cell[count], 0)

            # Draw text left
            qcol = self.font.render(self.text[count], True, cfg.BLACK)
            self.background.blit(qcol, (self.left_text_x, self.left_text_y + count * 50 + 100))
            count+=1

    def draw_static_text(self):
        # A function that draw static text

        count = 0
        while count < cfg.BOARD_SIZE[1]:
            # Draw text left
            qcol = self.font.render(self.text[count], True, cfg.BLACK)
            self.background.blit(qcol, (self.left_text_x, self.left_text_y + count * 50 + 100))
            count+=1



    def update(self, qs):
        # Update the elements for the main menu screen

        self.draw_title()

        # In this way the previous content is covered
        self.draw_cell()
        try:
            count = 0
            while count < cfg.BOARD_SIZE[1]:

                # Draw text right
                qcol_value = self.font.render(str(qs[count]), True, cfg.BLACK)
                self.background.blit(qcol_value, (self.right_text_x, self.right_text_y + count * 50 + 100))

                count+=1
        except:
            print("Eccezione Table")
