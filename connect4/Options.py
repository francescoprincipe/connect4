import pygame
import config as cfg
import imp
import sys

class Options(object):
    # A class where users can change game parameters

    def __init__(self, background, width):
        self.options_mode = False
        self.background = background
        self.width = width
        pass

    #--Setter--
    def set_options_mode(self, mode):
        self.options_mode = mode

    #--Getter--
    def get_options_mode(self):
        return self.options_mode

    def draw_options(self, games, speed, music, epsilon):
        font = pygame.font.SysFont('mono', 40, bold=True)
        color_txt = cfg.BLACK

        back_txt = "Back to menu"
        games_txt = "Training games: " + str(games)
        speed_txt = "Speed: " + str(speed)
        epsilon_txt ='Epsilon: '+ str(epsilon)
        music_txt = "Music: "

        if music == True:
            music_txt += "ON"
        else:
            music_txt += "OFF"


        self.background.fill(cfg.LIGHT_BLUE)
        cover_rect = pygame.Rect(self.width-890, 90, 570, 490)
        pygame.draw.rect(self.background, cfg.BLACK, cover_rect, 0)
        cover_rect = pygame.Rect(self.width-880, 100, 550, 470)
        pygame.draw.rect(self.background, cfg.LIGHT_BLUE1, cover_rect, 0)


        image = pygame.image.load("Title/Settings.png")
        #image = pygame.transform.scale(image, (303, 50))
        self.background.blit(image,((self.width-image.get_rect().size[0])//2,50) )

        surface = font.render(games_txt, True, color_txt)
        fw, fh = font.size(games_txt)
        self.rect_games = surface.get_rect(topleft=((self.width - fw) // 2, 225))
        self.background.blit(surface, ((self.width - fw) // 2, 225) )

        surface = font.render(speed_txt, True, color_txt)
        fw, fh = font.size(speed_txt)
        self.rect_speed = surface.get_rect(topleft=((self.width - fw) // 2, 275))
        self.background.blit(surface, ((self.width - fw) // 2, 275) )

        surface = font.render(epsilon_txt, True, color_txt)
        fw, fh = font.size(epsilon_txt)
        self.rect_epsilon = surface.get_rect(topleft=((self.width - fw) // 2, 325))
        self.background.blit(surface, ((self.width - fw) // 2, 325) )

        surface = font.render(music_txt, True, color_txt)
        fw, fh = font.size(music_txt)
        self.rect_music = surface.get_rect(topleft=((self.width - fw) // 2, 375))
        self.background.blit(surface, ((self.width - fw) // 2, 375) )

        surface = font.render(back_txt, True, color_txt)
        fw, fh = font.size(back_txt)
        self.rect_back = surface.get_rect(topleft=((self.width - fw) // 2, 445))
        self.background.blit(surface, ((self.width - fw) // 2, 445) )

    def running_options(self, games_number, speed_train, music, epsilon, screen, menu):

        while self.options_mode:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.isClickedGamesNumber(pygame.mouse.get_pos()):
                        games_number*=10
                        if(games_number>100000):
                            games_number=1
                        self.draw_options(games_number, speed_train, music, epsilon)

                    if self.isClickedSpeedTrain(pygame.mouse.get_pos()):
                        speed_train+=1
                        if(speed_train>20):
                            speed_train=0
                        self.draw_options(games_number, speed_train, music, epsilon)

                    if self.isClickedEpsilon(pygame.mouse.get_pos()):
                        epsilon+=0.1
                        if(epsilon>1):
                            epsilon=0
                        self.draw_options(games_number, speed_train, music, epsilon)


                    if self.isClickedMusic(pygame.mouse.get_pos()):
                        music = (not music)
                        if music==True:
                            pygame.mixer.music.load('music1.mp3')
                            pygame.mixer.music.play(-1)
                        if music == False:
                            pygame.mixer.music.stop()
                        self.draw_options(games_number, speed_train, music, epsilon)

                    if self.isClickedBack(pygame.mouse.get_pos()):
                        menu.set_menu_mode(True)
                        self.options_mode = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.options_mode = False
                        self.save_config(games_number, speed_train, music, epsilon)

                if event.type == pygame.QUIT:
                      menu.set_menu_mode(False)
                      self.options_mode= False
                      self.save_config(games_number, speed_train, music, epsilon)
                      exit()


            pygame.display.flip()
            screen.blit(self.background, (0, 0))

        if not (menu.get_menu_mode() or self.options_mode):
            self.save_config()
            pygame.quit()
            sys.exit(0)

        self.save_config(games_number, speed_train, music, epsilon)
        return (games_number, speed_train, music, epsilon)

    def save_config(self, games_number, speed_train, music, epsilon):

        with open("config.py", "r") as file:
            lines = file.readlines()

        lines[lines.index("EPSILON = " + str(cfg.EPSILON) + "\n")] = "EPSILON = " + str(epsilon) + "\n"
        lines[lines.index("GAMES_NUMBER = " + str(cfg.GAMES_NUMBER) + "\n")] = "GAMES_NUMBER = " + str(games_number) + "\n"
        lines[lines.index("SPEED_TRAIN = " + str(cfg.SPEED_TRAIN) + "\n")] = "SPEED_TRAIN = " + str(speed_train) + "\n"
        lines[lines.index("MUSIC = " + str(cfg.MUSIC) + "\n")] = "MUSIC = " + str(music) + "\n"

        with open("config.py", "w") as file:
            for line in lines:
                file.write(line)

        imp.reload(cfg)

    def isClickedGamesNumber(self, position):
        if self.rect_games.collidepoint(position):
            return True
        return False

    def isClickedSpeedTrain(self, position):
        if self.rect_speed.collidepoint(position):
            return True
        return False

    def isClickedMusic(self, position):
        if self.rect_music.collidepoint(position):
            return True
        return False

    def isClickedEpsilon(self, position):
        if self.rect_epsilon.collidepoint(position):
            return True
        return False

    def isClickedBack(self, position):
        if self.rect_back.collidepoint(position):
            return True
        return False
