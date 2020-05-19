from src.game_files.GameInitialisation import *
from src.game_files import Button
import time
from threading import Thread

class MainGame:
    def __init__(self):
        self.__leave_button = Button.Button((51, 51, 255), 700, 15, 50, 30, 21, "Leave")

    def end_func(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

    control_end_game = lambda self, player: False if player.is_alive else True

    control_end_level = lambda self, ghosts_list: True if not ghosts_list else False

    def handle_all_ghosts(self, ghosts_list):
        for g in ghosts_list:
            g.handle_movement()

    def set_labels_in_game(self, player, level):
        # upper info bar
        screen.blit(transparent_surface, (0, 0))
        print_label("Player's lifes:", 0, 0, 20)
        for x in range(0, player.health):
            screen.blit(heart, (x * 40, 20))
        print_label("Bombs amount: " + str(player.bomb_amount)
                    + "  Bombs' range: " + str(player.bomb_range)
                    + "  Level: " + str(level), 200, 15, 30)

    def leave_button_handler(self):
        self.__leave_button.draw(screen, (255, 255, 255))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.__leave_button.mouse_hover(pos):
                    return True
            if event.type == pygame.MOUSEMOTION:
                if self.__leave_button.mouse_hover(pos):
                    self.__leave_button.color = (51, 51, 200)


    def main_game(self, player, ghosts_list, level):
        last_time = time.time()
        last_time_collision_with_ghost = time.time()
        generate_map(game_map)
        place_stones()
        transparent_surface = pygame.Surface((750, 50))
        transparent_surface.set_alpha(128)
        while True:
            start_time = time.time()
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            screen.blit(transparent_surface, (0, 0))
            print_label("Player's lifes:", 0, 0, 20)
            for x in range(0, player.health):
                screen.blit(heart, (x * 40, 20))
            #show_stats(player, level, 400, 15)
            #print_label("Bombs amount/range: " + str(player.bomb_amount)
            #            + "Level: " + str(level), 200, 15, 30)
            #print_label("Bombs' range: " + str(player.bomb_range), 400, 15, 30)
            #print_label("Level: " + str(level), 600, 15, 30)
            print_label("Bombs amount: " + str(player.bomb_amount)
                        + "  Bombs' range: " + str(player.bomb_range)
                        + "  Level: " + str(level), 200, 15, 30)
            #thread_label = Thread(target=self.set_labels_in_game(player, level))
            #self.set_labels_in_game(player, level)
            place_stones()
            player.handle_movement()
            mark_player_on_map(player)
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
            player.check_explosion(ghosts_list, player.get_player_position_on_map())
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
