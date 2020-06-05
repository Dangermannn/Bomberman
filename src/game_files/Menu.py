import pygame
from src.game_files import Button
from src.game_files import Constants
from src.game_files import GameInitialisation as init

class Menu:
    def __init__(self, surface):
        self.__start_button = Button.Button(Constants.BLUE, 70, 70, 100, 50, 21, "Start game")
        self.__end_button = Button.Button(Constants.RED, 300, 70, 100, 50, 21, "Quit")
        self.__about_button = Button.Button(Constants.LIME, 500, 70, 100, 50, 21, "About game")
        self.__show_about = False
        self.__screen = surface

    def draw_menu(self):
        """
        Draws background and buttons in menu
        :return:
        """
        self.__screen.fill(pygame.Color("black"))
        self.__screen.blit(Constants.Assets.MENU_BACKGROUND_IMG, (0, 0))
        self.__start_button.draw(self.__screen, Constants.WHITE)
        self.__end_button.draw(self.__screen, Constants.WHITE)
        self.__about_button.draw(self.__screen, Constants.WHITE)

    def menu(self):
        """
        Main menu function that handles buttons
        """
        self.__show_about = False
        pygame.mixer.music.play(loops=-1)
        while True:
            self.draw_menu()
            init.print_about_game(self.__show_about, self.__screen)
            pygame.display.update()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__start_button.mouse_hover(pos):
                        pygame.mixer.music.stop()
                        pygame.mixer.music.rewind()
                        return
                    if self.__end_button.mouse_hover(pos):
                        pygame.quit()
                        quit()
                    if self.__about_button.mouse_hover(pos):
                        if not self.__show_about:
                            self.__show_about = True
                        else:
                            self.__show_about = False
                if event.type == pygame.MOUSEMOTION:
                    if self.__start_button.mouse_hover(pos):
                        self.__start_button.color = Constants.DARK_BLUE
                    else:
                        self.__start_button.color = Constants.BLUE
                    if self.__end_button.mouse_hover(pos):
                        self.__end_button.color = Constants.RED
                    else:
                        self.__end_button.color = Constants.BURGUNDY
                    if self.__about_button.mouse_hover(pos):
                        self.__about_button.color = Constants.DARK_GREEN
                    else:
                        self.__about_button.color = Constants.BRIGHT_GREEN
                        