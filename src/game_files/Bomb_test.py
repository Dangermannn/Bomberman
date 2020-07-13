import time
import unittest
import pygame
from src.game_files import Bomb
from src.game_files import Characters
from src.game_files import Constants
from src.game_files import GameInitialisation as init
"""
Module for bomb unit tests
"""
class BombTest(unittest.TestCase):
    """Class for bomb tests"""
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.mixer.init()
        cls.screen = pygame.display.set_mode((750, 750))
        Constants.Assets.load()
        cls.player = Characters.Player(cls.screen, 200, 150, 5, 6, 13, 13, Constants.HERO_IMG_PATH)
        cls.bomb = Bomb.Bomb(cls.screen, 50, 50, 3, 2)
        cls.ghost_1 = Characters.Ghost(cls.screen, 650, 50, 1, 4, 2, 1, Constants.WHITE_GHOST_PATH, Constants.EASY)
        cls.ghost_2 = Characters.Ghost(cls.screen, 50, 650, 1, 3, 2, 1, Constants.BLUE_GHOST_PATH, Constants.MEDIUM)
        cls.ghost_3 = Characters.Ghost(cls.screen, 650, 650, 1, 1, 1, 1, Constants.RED_GHOST_PATH, Constants.HARD)
        cls.ghosts_list = []
        init.generate_map(init.game_map)

    def test_is_intersection_true_4way(self):
        self.assertTrue(self.bomb.is_intersection(100, 250))

    def test_is_intersection_true_3way(self):
        self.assertTrue(self.bomb.is_intersection(250, 100))

    def test_is_intersection_true_right_down(self):
        self.assertTrue(self.bomb.is_intersection(50, 50))

    def test_is_intersection_true_left_down(self):
        self.assertTrue(self.bomb.is_intersection(150, 50))

    def test_is_intersection_true_right_up(self):
        self.assertTrue(self.bomb.is_intersection(50, 50))

    def test_is_intersection_true_left_up(self):
        self.assertTrue(self.bomb.is_intersection(650, 650))

    def test_is_intersection_false_left_right(self):
        self.assertFalse(self.bomb.is_intersection(100, 200))

    def test_is_vertical_true(self):
        self.assertTrue(self.bomb.is_vertical(100, 200))

    def test_is_vertical_false(self):
        self.assertFalse(self.bomb.is_vertical(150, 250))

    def test_is_horizontal_true(self):
        self.assertTrue(self.bomb.is_horizontal(150, 250))

    def test_is_horizontal_false(self):
        self.assertFalse(self.bomb.is_horizontal(100, 200))

    # Fire removes blocks / reduces hp
    def test_reduces_player_hp(self):
        temp = [self.player.health]
        bomb = Bomb.Bomb(self.screen, 50, 50, 3, 2)
        while not self.bomb.explosion(self.ghosts_list, self.player.get_player_position_on_map(),
                                      self.player.reduce_health_by_one):
            pass
        self.assertEqual(self.player.health, temp[0])

    def test_kills_ghost(self):
        self.ghosts_list.append(self.ghost_1)
        bomb = Bomb.Bomb(self.screen, 50, 50, 3, 2)
        while not bomb.explosion(self.ghosts_list, self.player.get_player_position_on_map(),
                                 self.player.reduce_health_by_one):
            pass
        self.assertNotEqual(len(self.ghosts_list), 3)

    def test_remove_block_true(self):
        self.ghosts_list = []
        self.ghosts_list.clear()
        self.ghosts_list.append(self.ghost_1)

        init.generate_map(init.game_map)
        bomb = Bomb.Bomb(self.screen, 150, 100, 10, 10)

        while not bomb.explosion(self.ghosts_list, self.player.get_player_position_on_map(),
                                 self.player.reduce_health_by_one):
            pass
        self.assertEqual(init.game_map[3][3], Constants.CLEAR)


    # getting blocks to destroy
    def test_blocks_to_destroy_down_true(self):
        bomb = Bomb.Bomb(self.screen, 250, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((5, 4), blocks)

    def test_blocks_to_destroy_right_true(self):
        bomb = Bomb.Bomb(self.screen, 250, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((6, 3), blocks)

    def test_blocks_to_destroy_left_true(self):
        bomb = Bomb.Bomb(self.screen, 250, 250, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((4, 5), blocks)

    def test_blocks_to_destroy_up_true(self):
        bomb = Bomb.Bomb(self.screen, 250, 250, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((5, 4), blocks)

    def test_blocks_to_destroy_down_false(self):
        bomb = Bomb.Bomb(self.screen, 150, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((3, 3), blocks)

    def test_blocks_to_destroy_right_false(self):
        bomb = Bomb.Bomb(self.screen, 150, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((3, 3), blocks)

    def test_blocks_to_destroy_left_false(self):
        bomb = Bomb.Bomb(self.screen, 150, 250, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((3, 5), blocks)

    def test_blocks_to_destroy_up_false(self):
        bomb = Bomb.Bomb(self.screen, 100, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        self.assertIn((2, 6), blocks)

if __name__ == "__main__":
    unittest.main()
