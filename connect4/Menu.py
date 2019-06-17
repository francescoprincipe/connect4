import pygame
import webbrowser
import config as cfg
import imp

class Menu (object):
## This class draws the elements for the main menu screen and handles relatives events

    def __init__(self, background, width, height, connect_mode):
        self.menu_mode = False
        self.background = background
        self.width = width
        self.height = height
        self.connect_mode = connect_mode
        pass

    #---Setter---
    def set_connect_mode(self, connect_mode):
        self.connect_mode = connect_mode
        self.save_config()
        self.draw_logo_mode()

    #--Getter--
    def get_menu_mode(self):
        return self.menu_mode

    #--Setter--
    def set_menu_mode(self, mode):
        self.menu_mode = mode

    def draw_menu(self):
        self.draw_logo_mode()
        self.draw_playing_mode()
        self.draw_training_mode()
        self.draw_settings()
        self.draw_authors()
        self.draw_references()

    def draw_logo_mode(self):
        cover_rect = pygame.Rect(80, (self.height) // 3 + 40, 620, 200)
        pygame.draw.rect(self.background, cfg.LIGHT_BLUE, cover_rect, 0)
        logo_img = pygame.image.load("Title/Connect{}.png".format(self.connect_mode))
        logo_img = pygame.transform.scale(logo_img, (579, 167))
        self.background.blit(logo_img,(90, (self.height) // 3 + 40))

        pygame.display.set_caption("Connect"+str(self.connect_mode))

    def draw_playing_mode(self):
        cover_rect = pygame.Rect(self.width-450, 70, 400, 260)
        pygame.draw.rect(self.background, cfg.BLACK, cover_rect, 0)
        cover_rect = pygame.Rect(self.width-440, 80, 380, 240)
        pygame.draw.rect(self.background, cfg.LIGHT_BLUE1, cover_rect, 0)

        image = pygame.image.load("Title/Playing-mode.png")
        image = pygame.transform.scale(image, (303, 50))
        self.background.blit(image,(self.width-400, 50) )

        image = pygame.image.load("Title/Multiplayer.png")
        self.rect_pmode1 = image.get_rect(topleft=(self.width-image.get_rect().size[0]-120, 120) )
        self.background.blit(image,(self.width-image.get_rect().size[0]-120, 120) )

        image = pygame.image.load("Title/Singleplayer.png")
        self.rect_pmode2 = image.get_rect(topleft=(self.width-image.get_rect().size[0]-110, 220) )
        self.background.blit(image,(self.width-image.get_rect().size[0]-110, 220) )

    def draw_training_mode(self):
        cover_rect = pygame.Rect(self.width-450, 370, 400, 260)
        pygame.draw.rect(self.background, cfg.BLACK, cover_rect, 0)
        cover_rect = pygame.Rect(self.width-440, 380, 380, 240)
        pygame.draw.rect(self.background, cfg.LIGHT_BLUE1, cover_rect, 0)

        image = pygame.image.load("Title/Training-mode.png".format(self.connect_mode))
        image = pygame.transform.scale(image, (303, 50))
        self.background.blit(image,(self.width-400, 350))

        image = pygame.image.load("Title/Teach-the-agents.png")
        self.rect_tmode1 = image.get_rect(topleft=(self.width-image.get_rect().size[0]-100, 420) )
        self.background.blit(image,(self.width-image.get_rect().size[0]-100, 420) )

        image = pygame.image.load("Title/Let-the-agents-learn.png")
        self.rect_tmode2 = image.get_rect(topleft=(self.width-image.get_rect().size[0]-70, 520) )
        self.background.blit(image,(self.width-image.get_rect().size[0]-70, 520) )

    def draw_settings(self):
        image = pygame.image.load("Title/options.png")
        self.rect_setting1 = image.get_rect(topleft=(self.width-80, 7))
        self.background.blit(image,(self.width-80, 7))

    def draw_references(self):
        color_txt = cfg.DARK_BLUE
        font = pygame.font.SysFont('arial', 15, bold=False)
        title_font = pygame.font.SysFont('arial', 20, bold=True)

        title = "References:"
        reference1 = "https://github.com/TesterDiscoverAI/Connect4AIGame"
        reference2 = "https://github.com/ShekMaha/connect4-reinforcement-learning/blob/master/connect4.py"

        surface = title_font.render(title, True, color_txt)
        fw, fh = title_font.size(title)
        self.background.blit(surface, (30 , 580))

        surface = font.render(reference1, True, color_txt)
        fw, fh = font.size(reference1)
        self.rect_reference1 = surface.get_rect(topleft=(30, 610))
        self.background.blit(surface, (30, 610) )

        surface = font.render(reference2, True, color_txt)
        fw, fh = font.size(reference2)
        self.rect_reference2 = surface.get_rect(topleft=(30, 630) )
        self.background.blit(surface, (30, 630) )

    def draw_authors(self):
        color_txt = cfg.DARK_BLUE
        font = pygame.font.SysFont('arial', 15, bold=False)
        title_font = pygame.font.SysFont('arial', 20, bold=True)

        title = "Created by:"
        author1 = "Francesco Periti"
        fb_author1 = "https://www.facebook.com/francesco.periti"
        author2 = "Francesco Principe"
        fb_author2 = "https://www.facebook.com/francesco.principe.75"

        surface = title_font.render(title, True, color_txt)
        fw, fh = title_font.size(title)
        self.background.blit(surface, (30, 50) )

        surface = font.render(author1, True, color_txt)
        fw, fh = font.size(author1)
        self.background.blit(surface, (30, 80) )
        self.rect_author1 = surface.get_rect(topleft=(30, 80))

        surface = font.render(author2, True, color_txt)
        fw, fh = font.size(author2)
        self.background.blit(surface, (30, 100) )
        self.rect_author2 = surface.get_rect(topleft=(30,100))

    def onClick(self, position, play_game, options, game_mode):

        if self.rect_author1.collidepoint(position):
            webbrowser.open("https://www.facebook.com/francesco.periti")

        if self.rect_author2.collidepoint(position):
            webbrowser.open("https://www.facebook.com/francesco.principe.75")

        if self.rect_reference1.collidepoint(position):
            webbrowser.open("https://github.com/TesterDiscoverAI/Connect4AIGame")

        if self.rect_reference2.collidepoint(position):
            webbrowser.open("https://github.com/ShekMaha/connect4-reinforcement-learning/blob/master/connect4.py")

        if self.isClickedMultiPlayer(position):
            play_game = True
            self.menu_mode = False
            options.set_options_mode(False)
            game_mode = "Multiplayer"

        if self.isClickedTeachAgents(position):
            play_game = True
            self.menu_mode = False
            options.set_options_mode(False)
            game_mode = "TeachAgents"

        if self.isClickedSinglePlayer(position):
            play_game = True
            self.menu_mode = False
            options.set_options_mode(False)
            game_mode = "Singleplayer"

        if self.isClickedAgentsLearn(position):
            play_game = True
            self.menu_mode = False
            options.set_options_mode(False)
            game_mode = "AgentsLearn"

        if self.isClickedOptions(position):
            game_mode = "Options"
            play_game = False
            self.menu_mode = False
            options.set_options_mode(True)

        return (play_game, game_mode)

    def onPress(self, key, options):
        if key == pygame.K_ESCAPE:
            self.menu_mode = False
            options.set_options_mode(False)
        if key == pygame.K_LEFT:
            if self.connect_mode == 2:
                self.set_connect_mode(4)
            else:
                self.set_connect_mode(self.connect_mode-1)


        if key == pygame.K_RIGHT:
            if self.connect_mode == 4:
                self.set_connect_mode(2)
            else:
                self.set_connect_mode(self.connect_mode+1)

        return self.connect_mode

    def isClickedSinglePlayer(self, position):
        if self.rect_pmode2.collidepoint(position):
            return True
        return False

    def isClickedMultiPlayer(self, position):
        if self.rect_pmode1.collidepoint(position):
            return True
        return False

    def isClickedOptions(self, position):
        if self.rect_setting1.collidepoint(position):
            return True
        return False

    def isClickedTeachAgents(self, position):
        if self.rect_tmode1.collidepoint(position):
            return True
        return False

    def isClickedAgentsLearn(self, position):
        if self.rect_tmode2.collidepoint(position):
            return True
        return False

    def save_config(self):
        with open("config.py", "r+") as file:
            lines = file.readlines()

        lines[lines.index("NAME_DB = \"connect" + str(cfg.CONNECT_MODE) + ".db\"\n")] = "NAME_DB = \"connect" + str(self.connect_mode) + ".db\"\n"
        lines[lines.index("CONNECT_MODE = " + str(cfg.CONNECT_MODE) + "\n")] = "CONNECT_MODE = " + str(self.connect_mode) + "\n"

        if self.connect_mode == 2:
            lines[lines.index("BOARD_SIZE = " + str(cfg.BOARD_SIZE) + "\n")] = "BOARD_SIZE = (2, 4)\n"
        if self.connect_mode == 3:
            lines[lines.index("BOARD_SIZE = " + str(cfg.BOARD_SIZE) + "\n")] = "BOARD_SIZE = (4, 5)\n"
        if self.connect_mode == 4:
            lines[lines.index("BOARD_SIZE = " + str(cfg.BOARD_SIZE) + "\n")] = "BOARD_SIZE = (6, 7)\n"

        with open("config.py", "w+") as file:
            for line in lines:
                file.write(line)

        imp.reload(cfg)
