import unittest, time
import pygame
from src.game_files import Characters
from src.game_files import Bomb
from src.game_files import Constants
from src.game_files import GameInitialisation as init

class GhostTest(unittest.TestCase):
    "Class for ghost tests"
    def setUp(self):
        pygame.init()
        pygame.mixer.init()
        self.player = Characters.Player(200, 150, 5, 6, 13, 13, Constants.HERO_IMG_PATH)
        self.bomb = Bomb.Bomb(50, 50, 3, 2)
        self.ghost_1 = Characters.Ghost(650, 50, 1, 4, 2, 1, Constants.WHITE_GHOST_PATH, Constants.EASY)
        self.ghost_2 = Characters.Ghost(50, 650, 1, 3, 2, 1, Constants.BLUE_GHOST_PATH, Constants.MEDIUM)
        self.ghost_3 = Characters.Ghost(650, 650, 1, 1, 1, 1, Constants.RED_GHOST_PATH, Constants.HARD)
        self.ghosts_list = []
        init.generate_map(init.game_map)

    def test_easy_ghost_movement(self):
        pos_x, pos_y = self.ghost_1.position_x, self.ghost_1.position_y
        before_time = time.time()
        while True:
            self.ghost_1.handle_movement()
            now = time.time()
            if now - before_time > 2:
                break
        temp = False

        if pos_x != self.ghost_1.position_x or pos_y != self.ghost_1.position_y:
            temp = True
        self.assertTrue(temp)

    def test_medium_ghost_movement(self):
        pos_x, pos_y = self.ghost_2.position_x, self.ghost_2.position_y
        before_time = time.time()
        while True:
            self.ghost_2.move_random_without_back()
            now = time.time()
            if now - before_time > 2:
                break
        temp = False

        if pos_x != self.ghost_2.position_x or pos_y != self.ghost_2.position_y:
            temp = True

        self.assertTrue(temp)

    def test_hard_ghost_movement(self):
        pos_x, pos_y = self.ghost_3.position_x, self.ghost_3.position_y
        init.game_map[1][1] = 'P'
        before_time = time.time()
        while True:
            self.ghost_3.following_player()
            now = time.time()
            if now - before_time > 5:
                break
        temp = False

        #print("CURRENT POS: ", g1.position_x, " ", g1.position_y)
        if pos_x != self.ghost_3.position_x or pos_y != self.ghost_3.position_y:
            temp = True
        self.assertTrue(temp)

if __name__ == "__main__":
    unittest.main()
