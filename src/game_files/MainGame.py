import time
import pygame
from threading import Thread
from pygame import mixer
from src.game_files import Button, Constants, GameInitialisation as init

class MainGame:
    def __init__(self):
        self.__leave_button = Button.Button((51, 51, 255), 700, 15, 50, 30, 21, "Leave")

    def end_func(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    control_end_game = lambda self, player: False if player.is_alive else True

    control_end_level = lambda self, ghosts_list: True if not ghosts_list else False

    def handle_all_ghosts(self, ghosts_list):
        for ghost in ghosts_list:
            ghost.handle_movement()

    def set_labels_in_game(self, player, level):
        """
        Function for settting upper labels
        :param player:
        :param level:
        :return:
        """
        # upper info bar
        #Constants.screen.blit(Constants.TRANSPARENT_SURFACE, (0, 0))
        init.print_label("Player's lifes:", 0, 0, 20)
        for x in range(0, player.health):
            Constants.screen.blit(Constants.HEART_IMG, (x * 40, 20))
        init.print_label("Bombs amount: " + str(player.bomb_amount)
                    + "  Bombs' range: " + str(player.bomb_range)
                    + "  Level: " + str(level), 200, 15, 30)

    def leave_button_handler(self):
        self.__leave_button.draw(Constants.screen, (255, 255, 255))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.__leave_button.mouse_hover(pos):
                    return True
            if event.type == pygame.MOUSEMOTION:
                if self.__leave_button.mouse_hover(pos):
                    self.__leave_button.color = (51, 51, 200)
        return False


    def main_game(self, player, ghosts_list, level):
        """
        Function for handing main game
        :param player: player object
        :param ghosts_list: list of ghosts
        :param level: current level
        :return: True if player loses, False it player wins
        """
        last_time = time.time()
        last_time_collision_with_ghost = time.time()
        init.generate_map(init.game_map)
        init.place_stones()
        transparent_surface = pygame.Surface((750, 50))
        transparent_surface.set_alpha(128)
        while True:
            start_time = time.time()
            Constants.screen.fill((0, 0, 0))
            Constants.screen.blit(Constants.BACKGROUND_IMG, (0, 0))
            Constants.screen.blit(transparent_surface, (0, 0))
            #init.print_label("Player's lifes:", 0, 0, 20)
            #for x in range(0, player.health):
            #    Constants.screen.blit(Constants.HEART_IMG, (x * 40, 20))
            #show_stats(player, level, 400, 15)
            #print_label("Bombs amount/range: " + str(player.bomb_amount)
            #            + "Level: " + str(level), 200, 15, 30)
            #print_label("Bombs' range: " + str(player.bomb_range), 400, 15, 30)
            #print_label("Level: " + str(level), 600, 15, 30)
            #init.print_label("Bombs amount: " + str(player.bomb_amount)
            #            + "  Bombs' range: " + str(player.bomb_range)
            #            + "  Level: " + str(level), 200, 15, 30)
            #thread_label = Thread(target=self.set_labels_in_game(player, level))
            self.set_labels_in_game(player, level)
            init.place_stones()
            player.handle_movement()
            init.mark_player_on_map(player)
            self.handle_all_ghosts(ghosts_list)
            if self.leave_button_handler():
                return True
            if last_time is not None:
                now = time.time()
                if now - last_time > 0.5:  # 0.5
                    if player.is_bomb_added_to_list():
                        last_time = now
            if time.time() - last_time_collision_with_ghost > 1.0:
                player.collision_with_ghosts(ghosts_list)
                last_time_collision_with_ghost = time.time()
            player.check_explosion(ghosts_list)
            player.set_bombs_on_map()
            end_time = (start_time - time.time()) * 1000
            self.end_func()
            # clock.tick(60)
            if self.control_end_game(player):
                lose_sound = mixer.Sound("Sounds/SadTrombone-GamingSoundEffect.wav")
                lose_sound.play()
                return True
            if self.control_end_level(ghosts_list):
                win_sound = mixer.Sound("Sounds/Victory-Sound Effect.wav")
                win_sound.play()
                return False
            pygame.display.update()
            pygame.time.wait(int(end_time))
