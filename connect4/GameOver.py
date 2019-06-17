import pygame
import webbrowser
import config as cfg
import imp

class GameOver(object):

    def __init__(self, background, width):
        self.background = background
        self.width = width
        self.game_over_mode = False
        self.game_over_screen = False

    def set_game_over(self, game_over_mode):
        self.game_over_mode = game_over_mode

    def set_game_over_screen(self, game_over_screen):
        self.game_over_screen = game_over_screen

    def get_game_over(self):
        return self.game_over_mode

    def game_over(self, winner, menu, screen):
        # Display the game over screen

        self.game_over_screen = True
        menu.set_menu_mode(False)

        self.background.fill(cfg.LIGHT_BLUE)
        self.draw_game_over(winner)

        while self.game_over_screen:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_back.collidepoint(pygame.mouse.get_pos()):
                        menu.set_menu_mode(True)
                        self.game_over_screen = False

                    elif self.rect_quit.collidepoint(pygame.mouse.get_pos()):
                        self.game_over_screen = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over_screen = False
                if event.type == pygame.QUIT:
                    self.game_over_screen = False

            pygame.display.flip()
            screen.blit(self.background, (0, 0))

        if not menu.get_menu_mode():
            pygame.quit()

    def draw_game_over(self, winner):
        # Draw the elements for the game over screen
        cover_rect = pygame.Rect((self.width ) // 2 -226, 160, 520, 350)
        pygame.draw.rect(self.background, cfg.BLACK, cover_rect, 0)
        cover_rect = pygame.Rect((self.width ) // 2-216, 170, 500, 330)
        pygame.draw.rect(self.background, cfg.LIGHT_BLUE1, cover_rect, 0)
        
        if winner=="RED":
            game_over_img = pygame.image.load('Title/Game-Over-red.png')
            self.background.blit(game_over_img,((self.width - 230) // 2, 110))
        elif winner=="YELLOW":
            game_over_img = pygame.image.load('Title/Game-Over-yellow.png')
            self.background.blit(game_over_img,((self.width - 230) // 2, 110))
        else:
            game_over_img = pygame.image.load('Title/Game-Over-tie.png')
            self.background.blit(game_over_img,((self.width - 230) // 2, 110))

        
        game_over_img = pygame.image.load('Title/Back-to-menu.png')
        self.rect_back = game_over_img.get_rect(topleft=((self.width - 100) // 2 -20, 280))
        self.background.blit(game_over_img,((self.width - 40) // 2 -100, 280))

        game_over_img = pygame.image.load('Title/Quit.png')
        self.rect_quit = game_over_img.get_rect(topleft=((self.width - 40) // 2 +10, 370))
        self.background.blit(game_over_img,((self.width - 40) // 2 +10, 370))
        
