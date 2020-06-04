import unittest
from src.game_files import Characters
from src.game_files import Constants
from src.game_files import GameInitialisation as init

class PlayerTest(unittest.TestCase):
    """
    Class for player tests
    """
    def setUp(self):
        self.player = Characters.Player(50, 50, 5, 6, 13, 13, Constants.HERO_IMG_PATH)
        init.generate_map(init.game_map)

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

if __name__ == "__main__":
    unittest.main()
