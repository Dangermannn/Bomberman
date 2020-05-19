import unittest

#Qfrom src.Characters.Player import *
#from src.Characters.Ghost import Ghost
#from src.GameInitialisation import *
#from src.GameInterface import MainGame
from src.Bomb import Bomb

class Tests(unittest.TestCase):
    """
    Tests for collisions
    """

    def test_collision_left_true(self):
        generate_map(game_map)
        p = Player(200, 150, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_x(p.position_x - 5), True)

    def test_collision_right_true(self):
        generate_map(game_map)
        p = Player(300, 150, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_x(p.position_x + 5), True)

    def test_collision_up_true(self):
        generate_map(game_map)
        p = Player(200, 100, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_y(p.position_y - 5), True)

    def test_collision_down_true(self):
        generate_map(game_map)
        p = Player(300, 150, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_y(p.position_y + 5), True)

    def test_collision_left_false(self):
        generate_map(game_map)
        p = Player(100, 250, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_x(p.position_x - 5), False)

    def test_collision_right_false(self):
        generate_map(game_map)
        p = Player(100, 250, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_x(p.position_x + 5), False)

    def test_collision_up_false(self):
        generate_map(game_map)
        p = Player(100, 250, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_y(p.position_y - 5), False)

    def test_collision_down_false(self):
        generate_map(game_map)
        p = Player(100, 250, 5, 6, 13, 13, 'Images/Hero.png')
        self.assertEqual(p.collision_y(p.position_y + 5), False)

    """
    Tests for checking if place on map is intersection or vertical/horizontal path
    """

    def test_is_intersection_true_4way(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_intersection(100, 250), True)

    def test_is_intersection_true_3way(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_intersection(250, 100), True)

    def test_is_intersection_true_right_down(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_intersection(50, 50), True)

    def test_is_intersection_true_left_down(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_intersection(150, 50), True)

    def test_is_intersection_true_right_up(self):
        generate_map(game_map)
        b = Bomb(50, 650, 3, 2)
        self.assertEqual(b.is_intersection(50, 50), True)

    def test_is_intersection_true_left_up(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_intersection(650, 650), True)

    def test_is_intersection_false_left_right(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_intersection(100, 200), False)

    def test_is_vertical_true(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_vertical(100, 200), True)

    def test_is_vertical_false(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_vertical(150, 250), False)

    def test_is_horizontal_true(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_horizontal(150, 250), True)

    def test_is_horizontal_false(self):
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)
        self.assertEqual(b.is_horizontal(100, 200), False)

    # Fire removes blocks / reduces hp
    def test_reduces_player_hp(self):
        ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
        g1 = Ghost(650, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
        g2 = Ghost(50, 650, 1, 3, 2, 1, 'Images/blueGhost.png', MEDIUM)
        g3 = Ghost(650, 650, 1, 1, 1, 1, 'Images/redGhost.png', HARD)
        ghosts_list = []
        ghosts_list.append(g1)
        ghosts_list.append(g2)
        ghosts_list.append(g3)
        generate_map(game_map)
        temp = [ch1.health]
        b = Bomb(50, 50, 3, 2)

        while (b.explosion(ghosts_list, ch1.get_player_position_on_map(), temp, ch1.is_alive) != True):
            pass

        self.assertEqual(ch1.health == temp, False)

    def test_kills_ghost(self):
        ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
        g5 = Ghost(50, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
        ghosts_list = []
        ghosts_list.append(g5)
        generate_map(game_map)
        b = Bomb(50, 50, 3, 2)

        while (b.explosion(ghosts_list, ch1.get_player_position_on_map(), ch1.health, ch1.is_alive) != True):
            pass
        temp = (len(ghosts_list) != 3)
        self.assertEqual(temp, True)

    def test_remove_block_true(self):
        ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
        g1 = Ghost(650, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
        ghosts_list = []
        ghosts_list.append(g1)

        generate_map(game_map)
        b = Bomb(150, 100, 10, 10)

        while (b.explosion(ghosts_list, ch1.get_player_position_on_map(), ch1.health, ch1.is_alive) != True):
            pass

        temp3 = False
        if game_map[3][3] == ' ':
            temp3 = True

        self.assertEqual(temp3, True)

    # def test_move_to_next_level(self):
    #     ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
    #     g1 = Ghost(50, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
    #     ghosts_list = []
    #     ghosts_list.append(g1)
    #     generate_map(game_map)
    #     m = MainGame()
    #
    #     temp = [ch1.health]
    #     b = Bomb(50, 50, 3, 2)
    #
    #     while (b.explosion(ghosts_list, ch1.get_player_position_on_map(), temp, ch1.is_alive) != True):
    #         pass
    #     temp = m.control_end_game(ghosts_list)
    #     self.assertEqual(temp, True)

    # uzyskanie bloków do zniszczenia
    def test_blocks_to_destroy_down_true(self):
        generate_map(game_map)
        b = Bomb(250, 150, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (5, 4) in blocks:
            temp = True

        self.assertEqual(temp, True)

    def test_blocks_to_destroy_right_true(self):
        generate_map(game_map)
        b = Bomb(250, 150, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (6, 3) in blocks:
            temp = True

        self.assertEqual(temp, True)

    def test_blocks_to_destroy_left_true(self):
        generate_map(game_map)
        b = Bomb(250, 250, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (4, 5) in blocks:
            temp = True

        self.assertEqual(temp, True)

    def test_blocks_to_destroy_up_true(self):
        generate_map(game_map)
        b = Bomb(250, 250, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (5, 4) in blocks:
            temp = True

        self.assertEqual(temp, True)

    #################

    def test_blocks_to_destroy_down_false(self):
        generate_map(game_map)
        b = Bomb(150, 150, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (3, 2) in blocks:
            temp = True

        self.assertEqual(temp, False)

    def test_blocks_to_destroy_right_false(self):
        generate_map(game_map)
        b = Bomb(50, 50, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (2, 1) in blocks:
            temp = True

        self.assertEqual(temp, False)

    def test_blocks_to_destroy_left_false(self):
        generate_map(game_map)
        b = Bomb(150, 250, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (2, 1) in blocks:
            temp = True

        self.assertEqual(temp, False)

    def test_blocks_to_destroy_up_false(self):
        generate_map(game_map)
        b = Bomb(100, 150, 5, 5)
        blocks = []
        b.get_explosion_blocks(blocks)
        print(blocks)
        temp = False
        if (2, 4) in blocks:
            temp = True

        self.assertEqual(temp, False)


    # test if ghosts moves
    def test_easy_ghost_movement(self):
        ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
        g1 = Ghost(650, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
        pos_x, pos_y = g1.position_x, g1.position_y
        generate_map(game_map)
        before_time = time.time()
        while True:
            g1.handle_movement()
            now = time.time()
            if now - before_time > 2:
                break
        temp = False

        if pos_x != g1.position_x or pos_y != g1.position_y:
            temp = True

        self.assertEqual(temp, True)

    def test_medium_ghost_movement(self):
        ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
        g1 = Ghost(650, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', MEDIUM)
        pos_x, pos_y = g1.position_x, g1.position_y
        generate_map(game_map)
        before_time = time.time()
        while True:
            g1.move_random_without_back()
            now = time.time()
            if now - before_time > 2:
                break
        temp = False

        if pos_x != g1.position_x or pos_y != g1.position_y:
            temp = True

        self.assertEqual(temp, True)
    
    def test_hard_ghost_movement(self):
        print("INITIALIS")
        g1 = Ghost(650, 650, 1, 4, 2, 1, 'Images/whiteGhost.png', HARD)
        pos_x, pos_y = g1.position_x, g1.position_y
        game_map[1][1] = 'P'
        before_time = time.time()

        while True:
            g1.following_player()
            now = time.time()
            if now - before_time > 5:
                break

        temp = False

        print("CURRENT POS: ", g1.position_x, " ", g1.position_y)
        if pos_x != g1.position_x or pos_y != g1.position_y:
            temp = True

        self.assertEqual(temp, True)



    # Test for checking whether player's position on map is marked properly (letter 'P')

    def test_marking_player_on_map(self):
        ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
        generate_map(game_map)
        temp = False
        mark_player_on_map(ch1)
        ch1.position_x = 100
        mark_player_on_map(ch1)

        if game_map[1][1] == ' ' and game_map[2][1] == 'P':
            temp = True

        self.assertEqual(temp, True)