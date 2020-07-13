import time
import unittest
import pygame
from src.game_files import Characters
from src.game_files import Constants
from src.game_files import GameInitialisation as init

"""
Module for testing characters
"""

class PlayerTest(unittest.TestCase):
    """
    Class for player tests
    """
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((750, 750))
        Constants.Assets.load()
        init.generate_map(init.game_map)

    def setUp(self):
        self.player = Characters.Player(self.screen, 50, 50, 5, 6, 13, 13, Constants.HERO_IMG_PATH)

    def test_marking_player_on_map(self):
        temp = False
        init.mark_player_on_map(self.player)
        self.player.position_x = 100
        init.mark_player_on_map(self.player)

        if init.game_map[1][1] == ' ' and init.game_map[2][1] == 'P':
            temp = True
        self.assertTrue(temp)

    def test_collision_left_true(self):
        self.player.position_x = 200
        self.player.position_y = 200
        self.assertTrue(self.player.collision_x(self.player.position_x - 5))

    def test_collision_right_true(self):
        self.player.position_x = 300
        self.player.position_y = 150
        self.assertTrue(self.player.collision_x(self.player.position_x + 5))

    def test_collision_up_true(self):
        self.player.position_x = 200
        self.player.position_y = 100
        self.assertTrue(self.player.collision_y(self.player.position_y - 5))

    def test_collision_down_true(self):
        self.player.position_x = 300
        self.player.position_y = 150
        self.assertTrue(self.player.collision_y(self.player.position_y + 5))

    def test_collision_left_false(self):
        self.player.position_x = 100
        self.player.position_y = 250
        self.assertFalse(self.player.collision_x(self.player.position_x - 5))

    def test_collision_right_false(self):
        self.player.position_x = 100
        self.player.position_y = 250
        self.assertFalse(self.player.collision_x(self.player.position_x + 5))

    def test_collision_up_false(self):
        self.player.position_x = 100
        self.player.position_y = 250
        self.assertFalse(self.player.collision_y(self.player.position_y - 5))

    def test_collision_down_false(self):
        self.player.position_x = 100
        self.player.position_y = 250
        self.assertFalse(self.player.collision_y(self.player.position_y + 5))

class GhostTest(unittest.TestCase):
    "Class for ghost tests"
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.mixer.init()
        cls.screen = pygame.display.set_mode((750, 750))
        Constants.Assets.load()
        cls.ghost_1 = Characters.Ghost(cls.screen, 650, 50, 1, 4, 2, 1, Constants.WHITE_GHOST_PATH, Constants.EASY)
        cls.ghost_2 = Characters.Ghost(cls.screen, 50, 650, 1, 3, 2, 1, Constants.BLUE_GHOST_PATH, Constants.MEDIUM)
        cls.ghost_3 = Characters.Ghost(cls.screen, 650, 650, 1, 1, 1, 1, Constants.RED_GHOST_PATH, Constants.HARD)
        cls.ghosts_list = []
        init.generate_map(init.game_map)

    def test_easy_ghost_movement(self):
        pos_x, pos_y = self.ghost_1.position_x, self.ghost_1.position_y
        before_time = time.time()
        while True:
            self.ghost_1.handle_movement()
            now = time.time()
            if now - before_time > 2:
                break
        self.assertNotEqual((pos_x, pos_y), (self.ghost_1.position_x, self.ghost_1.position_y))

    def test_medium_ghost_movement(self):
        pos_x, pos_y = self.ghost_2.position_x, self.ghost_2.position_y
        before_time = time.time()
        while True:
            self.ghost_2.move_random_without_back()
            now = time.time()
            if now - before_time > 2:
                break
        self.assertNotEqual((pos_x, pos_y), (self.ghost_2.position_x, self.ghost_2.position_y))

    def test_hard_ghost_movement(self):
        pos_x, pos_y = self.ghost_3.position_x, self.ghost_3.position_y
        init.game_map[1][1] = 'P'
        before_time = time.time()
        while True:
            self.ghost_3.following_player()
            now = time.time()
            if now - before_time > 5:
                break
        self.assertNotEqual((pos_x, pos_y), (self.ghost_1.position_x, self.ghost_1.position_y))

if __name__ == "__main__":
    unittest.main()
