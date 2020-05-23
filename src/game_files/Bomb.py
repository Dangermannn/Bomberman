from pygame import mixer
from src.game_files import SpriteTool
from src.game_files.GameInitialisation import *
import time

class Bomb:
    INTERSECTION = 0
    STRAIGHT = 7
    END_STRIGHT = 14
    VERTICAL = 1
    HORIZONTAL = 2
    def __init__(self, position_x, position_y, range_field, set_time):
        self.position_x = position_x
        self.position_y = position_y
        self.range_field = range_field
        self.bomb_image = pygame.transform.scale((BOMB_IMAGE.convert_alpha()), (45, 45))
        self.bomb_sprite = SpriteTool.SpriteTool("Images/BombSprit.png", 7, 3)
        self.fire_blocks = []
        self.destroyed_blocks = []
        self.set_time = time.time()
        self.animation_step = 0
        self.last_animation_time = time.time()
        self.show_bomb = True
        self.explosion_sound = mixer.Sound('Sounds/bombExplosion.wav')

    def is_intersection(self, x, y):
        """
        Checking if  on coordinates (x, y) is an intersection. It is if it has:
        - 4 ways
        - 3 ways(left and (upper or down) or right and (upper or down))
        :param x: coordinate x
        :param y: coordinate y
        :return: True if it's intersection
        """
        left = x
        right = x + 2 * BLOCK_SIZE
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        free_sides = 0
        left_side = False
        right_side = False
        upper_side = False
        down_side = False
        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != WALL):
            left_side = True
            free_sides += 1
        if (game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != WALL):
            right_side = True
            free_sides += 1
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != WALL):
            upper_side = True
            free_sides += 1
        if (game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != WALL):
            down_side = True
            free_sides += 1

        if free_sides >= 3:
            return True
        elif (left_side and  (upper_side or down_side))  or (right_side and (upper_side or down_side)):
            return True
        return False

    def is_vertical(self, x, y):
        """
        Checking if  on coordinates (x, y) is an vertical path.
        :param x: coordinate x
        :param y: coordinate y
        :return: True if it's vertical path
        """
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != WALL) or (
                game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != WALL):
            return True
        return False

    def is_horizontal(self, x, y):
        """
        Checking if  on coordinates (x, y) is an horizontal path.
        :param x: coordinate x
        :param y: coordinate y
        :return: True if it's horizontal path
        """
        left = x
        right = x + 2 * BLOCK_SIZE
        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != WALL) or (
                game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != WALL):
            return True
        return False

    def get_explosion_blocks_downward(self, blocks_to_destroy, current_x, start_point_y):
        i = start_point_y
        iteration = 0
        while True:
            if game_map[current_x][i] == STONE:
                game_map[current_x][i] == CLEAR
                blocks_to_destroy.append((current_x, i))
                break
            if game_map[current_x][i] == WALL:
                break;
            if iteration > self.range_field:
                break
            if game_map[current_x][i] == CLEAR:
                if self.is_intersection(current_x * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((current_x * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(current_x * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((current_x * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(current_x * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((current_x * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += 1
            iteration += 1

    def get_explosion_blocks_upward(self, blocks_to_destroy, current_x, start_point_y):
        i = start_point_y
        iteration = 0
        while True:
            if game_map[current_x][i] == STONE:
                game_map[current_x][i] == CLEAR
                blocks_to_destroy.append((current_x, i))
                break
            if game_map[current_x][i] == WALL:
                break
            if iteration > self.range_field:
                break
            if game_map[current_x][i] == CLEAR:
                if self.is_intersection(current_x * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((current_x * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(current_x * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((current_x * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(current_x * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((current_x * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i -= 1
            iteration += 1

    def get_explosion_blocks_left(self, blocks_to_destroy, current_y, start_point_x):
        i = start_point_x
        iteration = 0
        while True:
            if game_map[i][current_y] == STONE:
                game_map[i][current_y] == CLEAR
                blocks_to_destroy.append((i, current_y))
                break
            if game_map[i][current_y] == WALL:
                break
            if iteration > self.range_field:
                break
            if game_map[i][current_y] == CLEAR:
                if self.is_intersection(i * BLOCK_SIZE, current_y * BLOCK_SIZE) == True:
                    self.fire_blocks.append((i * BLOCK_SIZE, current_y * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(i * BLOCK_SIZE, current_y * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, current_y * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(i * BLOCK_SIZE, current_y * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, current_y * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i -= 1
            iteration += 1

    def get_explosion_blocks_right(self, blocks_to_destroy, current_y, start_point_x):
        i = start_point_x
        iteration = 0
        while True:
            if game_map[i][current_y] == STONE:
                game_map[i][current_y] == CLEAR
                blocks_to_destroy.append((i, current_y))
                break
            if game_map[i][current_y] == WALL:
                break
            if iteration > self.range_field:
                break
            if game_map[i][current_y] == CLEAR:
                if self.is_intersection(i * BLOCK_SIZE, current_y * BLOCK_SIZE) == True:
                    self.fire_blocks.append((i * BLOCK_SIZE, current_y * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(i * BLOCK_SIZE, current_y * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, current_y * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(i * BLOCK_SIZE, current_y * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, current_y * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += 1
            iteration += 1

    def get_explosion_blocks(self, blocks_to_destroy):
        """
        Function scanning vertically and horizontally blocks, where it should place fire animation of the bomb
        CAUTION: IT RETURNS BLOCKS AS A LIST IN THROUGH THE PARAMETER
        :param blocks_to_destroy: Output list
        """
        start_iter_x = (self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1
        start_iter_y = (self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1

        self.get_explosion_blocks_downward(blocks_to_destroy, start_iter_x, start_iter_y)
        self.get_explosion_blocks_upward(blocks_to_destroy, start_iter_x, start_iter_y)
        self.get_explosion_blocks_left(blocks_to_destroy, start_iter_y, start_iter_x)
        self.get_explosion_blocks_right(blocks_to_destroy, start_iter_y, start_iter_x)

    def explosion(self, ghosts, playerCords, health, is_alive):
        """
        Handling explosion
        :param ghosts: list of ghosts
        :param playerCords: player coordinates
        :param health: player's health
        :param is_alive: player is_alive stat
        :return: True if it exploded
        """
        if self.animation_step == 0:
            self.get_explosion_blocks(self.destroyed_blocks)
        explosion_timer = time.time()
        if explosion_timer - self.set_time > 2:
            if self.animation_step == 0:
                self.explosion_sound.play()
            self.show_bomb = False
            if time.time() - self.last_animation_time > 0.05:
                self.animation_step += 1
                self.last_animation_time = time.time()
            for x in self.fire_blocks:
                if x[3] == self.VERTICAL:
                    self.bomb_sprite.draw_vertical(screen, (self.animation_step % 7) + x[2], x[0], x[1])
                else:
                    self.bomb_sprite.draw(screen, (self.animation_step % 7) + x[2], x[0], x[1])
                if self.animation_step % 7 == 6:
                    if self.is_collision_with_player(playerCords):
                        health[0] -= 1
                    self.is_collision_with_ghost(ghosts)
                    self.fire_blocks.clear()
                    for x, y in self.destroyed_blocks:
                        game_map[x][y] = CLEAR
                    self.destroyed_blocks.clear()
                    return True
        return False

    def get_bomb_position_on_map(self):
        """
        :return: Position coordinates on map (NOT PIXELS)
        """
        x = ((self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1)
        return (x, y)

    def get_fireblocks_position(self):
        """
        :return: List of fireblocks positions
        """
        ret = []
        for x in self.fire_blocks:
            ret.append((x[0] // BLOCK_SIZE, x[1] // BLOCK_SIZE))
        return ret

    def is_collision_with_ghost(self, ghosts):
        """
        Handling collision with ghosts, if it is reduces it's hp. If it's hp is 0 -> removes it from the list
        :param ghosts: list of ghosts
        """
        blocks = self.get_fireblocks_position()
        for g in ghosts:
            pos = []
            pos = g.get_border_positions_on_map()
            for p in pos:
                if p in blocks:
                    g.reduce_health_by_one()
                    if g.health == 0:
                        g.is_alive = False
                        ghosts.remove(g)

    def is_collision_with_player(self, coords):
        """
        Handling collision with a player
        :param coords: player coordinates
        :return: True if it's collision
        """
        blocks = self.get_fireblocks_position()
        for b in blocks:
            if b in coords:
                return True
        return False

    def set_position(self, position_x, position_y):
        screen.blit(self.bomb_image, (position_x, position_y))
