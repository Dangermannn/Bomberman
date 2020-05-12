from src.GameInitialisation import *
from src.Characters.Player import *
from src.Characters.Ghost import *
from src.Tools.Button import *
import pygame
import time
from pygame.locals import *
from pygame import mixer
import tracemalloc
from src.Tools.SpriteTool import SpriteTool
from threading import Thread

class MainGame:

    def __init__(self):
        pass

    def endfunc(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

    # def control_end_game(self, player):
    #     """
    #     If player is alive - returns false
    #     :param player: player object
    #     :return:
    #     """
    #     if player.is_alive:
    #         return False
    #     return True
    #
    # def control_end_level(self, ghosts_list):
    #     """
    #     If there's no ghost - returns false
    #     :return:
    #     """
    #     if not ghosts_list:
    #
    #         return True
    #     return False
    
    control_end_game = lambda self, player : False if player.is_alive else True

    control_end_level = lambda self, ghosts_list : True if not ghosts_list else False

    def handle_all_ghosts(self,ghost_list):
        for g in ghosts_list:
            g.handle_movement()

    def set_labels_in_game(self, player, level):
        # upper info bar
        transparent_surface = pygame.Surface((750, 50))
        transparent_surface.set_alpha(128)
        screen.blit(transparent_surface, (0, 0))
        print_label("Player's lifes:", 0, 0, 20)
        for x in range(0, player.health):
            screen.blit(heart, (x * 40, 20))
        print_label("Bombs amount: " + str(player.bomb_amount), 200, 15, 30)
        print_label("Bombs' range: " + str(player.bomb_range), 400, 15, 30)
        print_label("Level: " + str(level), 600, 15, 30)

    def main_game(self, player, ghosts_list, level):
        last_time = time.time()
        last_time_collision_with_ghost = time.time()
        explosion_step = 0
        leaveButton = Button((51, 51, 255), 700, 15, 50, 30, 21, "Leave")
        while True:
            start_time = time.time()
            # screen.fill((0, 0, 0))
            screen.fill(pygame.Color("black"))
            screen.blit(background, (0, 0))

            # leaveButton.draw(screen, (255, 255, 255))

            place_stones()

            # upper info bar
            thread_label = Thread(target=self.set_labels_in_game(player, level))
            # set_labels_in_game(ch1, level)
            # thread_player = Thread(target=player.handle_movement())
            # thread_player.start()
            # thread_player.join()
            player.handle_movement()
            # cord = player.get_player_position_on_map()
            # game_map[cord[0]][cord[1]] = 'P'
            # game_map[player.last_position_on_map[0], player.last_position_on_map[1]] = ' '
            # player.last_position_on_map = cord;
            mark_player_on_map(player)
            # print("GAME: ", game_map[player.last_position[0]][player.last_position[1]])
            # thread_ghosts = Thread(target=handle_all_ghosts(ghost_list))
            # thread_ghosts.start()

            for g in ghosts_list:
                #     thread_ghost = Thread(target=g.handle_movement())
                g.handle_movement()
            #    thread_ghost.start()
            # for x in game_map:
            # print(game_map)
            if last_time != None:
                now = time.time()
                if now - last_time > 0.5:  # 0.5
                    if player.is_bomb_added_to_list():
                        last_time = now
            if time.time() - last_time_collision_with_ghost > 1.0:
                player.collision_with_ghosts(ghosts_list)
                last_time_collision_with_ghost = time.time()

            player.check_explosion(ghosts_list, lambda: player.get_player_position_on_map())
            player.set_bombs_on_map()

            end_time = (start_time - time.time()) * 1000;
            self.endfunc()
            # thread_player.join()
            # thread_ghost.join()
            pygame.display.update()
            pygame.time.wait(int(end_time))
            # clock.tick(60)
            if self.control_end_game(player):
                loseSound = mixer.Sound("Sounds/SadTrombone-GamingSoundEffect.wav")
                loseSound.play()
                return True
            if self.control_end_level(ghosts_list):
                winSound = mixer.Sound("Sounds/Victory-Sound Effect.wav")
                winSound.play()
                return False