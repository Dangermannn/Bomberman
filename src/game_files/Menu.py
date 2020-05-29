import pygame
from pygame import mixer
from src.game_files import Button, Constants
from src.game_files import GameInitialisation as init

class Menu:
    def __init__(self):
        self.__start_button = Button.Button((51, 51, 255), 70, 70, 100, 50, 21, "Start game")
        self.__end_button = Button.Button((255, 0, 0), 300, 70, 100, 50, 21, "Quit")
        self.__about_button = Button.Button((51, 255, 51), 500, 70, 100, 50, 21, "About game")
        self.__show_about = False

    def draw_menu(self):
        """
        Draws background and buttons in menu
        :return:
        """
        Constants.screen.fill(pygame.Color("black"))
        Constants.screen.blit(Constants.MENU_BACKGROUND_IMG, (0, 0))
        self.__start_button.draw(Constants.screen, (0, 0, 0))
        self.__end_button.draw(Constants.screen, (255, 255, 255))
        self.__about_button.draw(Constants.screen, (255, 255, 255))

    def menu(self):
        """
        Main menu function that handles buttons
        """
        self.__show_about = False
        mixer.music.play(loops=-1)
        while True:
            self.draw_menu()
            init.print_about_game(self.__show_about)
            pygame.display.update()
            # self.self.__start_button.blitBut()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__start_button.mouse_hover(pos):
                        mixer.music.stop()
                        mixer.music.rewind()
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
                        self.__start_button.color = (10, 10, 150)
                    else:
                        self.__start_button.color = (51, 51, 255)
                    if self.__end_button.mouse_hover(pos):
                        self.__end_button.color = (255, 0, 0)
                    else:
                        self.__end_button.color = (150, 0, 0)
                    if self.__about_button.mouse_hover(pos):
                        self.__about_button.color = (51, 170, 51)
                    else:
                        self.__about_button.color = (51, 255, 51)
                        