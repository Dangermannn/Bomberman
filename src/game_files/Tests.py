import unittest, time
from src.game_files import Characters, Bomb, Constants, GameInitialisation as init
"""
Module for unit tests
"""
class BombTest(unittest.TestCase):
    """Class for bomb tests"""
    def setUp(self):
        self.player = Characters.Player(200, 150, 5, 6, 13, 13, Constants.HERO_IMG_PATH)
        self.bomb = Bomb.Bomb(50, 50, 3, 2)
        self.ghost_1 = Characters.Ghost(650, 50, 1, 4, 2, 1, Constants.WHITE_GHOST_PATH, Constants.EASY)
        self.ghost_2 = Characters.Ghost(50, 650, 1, 3, 2, 1, Constants.BLUE_GHOST_PATH, Constants.MEDIUM)
        self.ghost_3 = Characters.Ghost(650, 650, 1, 1, 1, 1, Constants.RED_GHOST_PATH, Constants.HARD)
        self.ghosts_list = []
        init.generate_map(init.game_map)

    """
    Tests for checking if place on map is intersection or vertical/horizontal path
    """

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
        bomb = Bomb.Bomb(50, 50, 3, 2)
        while not self.bomb.explosion(self.ghosts_list, self.player.get_player_position_on_map(), temp, self.player.is_alive):
            pass
        self.assertFalse(self.player.health == temp)

    def test_kills_ghost(self):
        self.ghosts_list.append(self.ghost_1)
        bomb = Bomb.Bomb(50, 50, 3, 2)
        while not bomb.explosion(self.ghosts_list, self.player.get_player_position_on_map(), self.player.health, self.player.is_alive):
            pass
        temp = (len(self.ghosts_list) != 3)
        self.assertTrue(temp)

    def test_remove_block_true(self):
        self.ghosts_list = []
        self.ghosts_list.clear()
        self.ghosts_list.append(self.ghost_1)

        init.generate_map(init.game_map)
        bomb = Bomb.Bomb(150, 100, 10, 10)

        while not bomb.explosion(self.ghosts_list, self.player.get_player_position_on_map(), self.player.health, self.player.is_alive):
            pass
        temp3 = False
        if init.game_map[3][3] == ' ':
            temp3 = True
        self.assertTrue(temp3, True)

    # getting blocks to destroy
    def test_blocks_to_destroy_down_true(self):
        bomb = Bomb.Bomb(250, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        temp = False
        if (5, 4) in blocks:
            temp = True
        self.assertTrue(temp)

    def test_blocks_to_destroy_right_true(self):
        bomb = Bomb.Bomb(250, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        temp = False
        if (6, 3) in blocks:
            temp = True
        self.assertTrue(temp, True)

    def test_blocks_to_destroy_left_true(self):
        bomb = Bomb.Bomb(250, 250, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        temp = False
        if (4, 5) in blocks:
            temp = True
        self.assertTrue(temp)

    def test_blocks_to_destroy_up_true(self):
        bomb = Bomb.Bomb(250, 250, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        temp = False
        if (5, 4) in blocks:
            temp = True
        self.assertTrue(temp)

    def test_blocks_to_destroy_down_false(self):
        bomb = Bomb.Bomb(150, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (3, 2) in blocks:
            temp = True
        self.assertFalse(temp)

    def test_blocks_to_destroy_right_false(self):
        bomb = Bomb.Bomb(50, 50, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (2, 1) in blocks:
            temp = True
        self.assertFalse(temp)

    def test_blocks_to_destroy_left_false(self):
        bomb = Bomb.Bomb(150, 250, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        temp = False
        if (2, 1) in blocks:
            temp = True
        self.assertFalse(temp)

    def test_blocks_to_destroy_up_false(self):
        bomb = Bomb.Bomb(100, 150, 5, 5)
        blocks = []
        bomb.get_explosion_blocks(blocks)
        temp = False
        if (2, 4) in blocks:
            temp = True
        self.assertFalse(temp)

class GhostTest(unittest.TestCase):
    "Class for ghost tests"
    def setUp(self):
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
