import pygame
from pygame import mixer
from src.game_files import SpriteTool, Constants
from src.game_files import GameInitialisation as init
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
        self.bomb_image = pygame.transform.scale((Constants.BOMB_IMAGE.convert_alpha()), (45, 45))
        self.bomb_sprite = SpriteTool.SpriteTool(Constants.BOMB_SPRITE_PATH, 7, 3)
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
        right = x + 2 * Constants.BLOCK_SIZE
        down = y + Constants.BLOCK_SIZE
        up = y - Constants.BLOCK_SIZE
        free_sides = 0
        left_side = False
        right_side = False
        upper_side = False
        down_side = False
        if (init.game_map[left // Constants.BLOCK_SIZE - 1][y // Constants.BLOCK_SIZE] != Constants.WALL):
            left_side = True
            free_sides += 1
        if (init.game_map[right // Constants.BLOCK_SIZE - 1][y // Constants.BLOCK_SIZE] != Constants.WALL):
            right_side = True
            free_sides += 1
        if (init.game_map[x // Constants.BLOCK_SIZE][up // Constants.BLOCK_SIZE] != Constants.WALL):
            upper_side = True
            free_sides += 1
        if (init.game_map[x // Constants.BLOCK_SIZE][down // Constants.BLOCK_SIZE] != Constants.WALL):
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
        down = y + Constants.BLOCK_SIZE
        up = y - Constants.BLOCK_SIZE
        if (init.game_map[x // Constants.BLOCK_SIZE][up // Constants.BLOCK_SIZE] != Constants.WALL) or (
                init.game_map[x // Constants.BLOCK_SIZE][down // Constants.BLOCK_SIZE] != Constants.WALL):
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
        right = x + 2 * Constants.BLOCK_SIZE
        if (init.game_map[left // Constants.BLOCK_SIZE - 1][y // Constants.BLOCK_SIZE] != Constants.WALL) or (
                init.game_map[right // Constants.BLOCK_SIZE - 1][y // Constants.BLOCK_SIZE] != Constants.WALL):
            return True
        return False

    def get_explosion_blocks_vertically(self, blocks_to_destroy, current_x, start_point_y, direction):
        """
        Function scanning horizontally blocks, where it should place fire animation of the bomb
        CAUTION: IT RETURNS BLOCKS AS A LIST IN THROUGH THE PARAMETER
        :param blocks_to_destroy: output list
        :param directiony: -1 if up, 1 if down
        """
        i = start_point_y
        iteration = 0
        while True:
            if init.game_map[current_x][i] == Constants.STONE:
                init.game_map[current_x][i] == Constants.CLEAR
                blocks_to_destroy.append((current_x, i))
                break
            if init.game_map[current_x][i] == Constants.WALL:
                break
            if iteration > self.range_field:
                break

            if init.game_map[current_x][i] == Constants.CLEAR:
                if self.is_intersection(current_x * Constants.BLOCK_SIZE, i * Constants.BLOCK_SIZE):
                    self.fire_blocks.append(
                        init.Fire_tuple(current_x * Constants.BLOCK_SIZE, i * Constants.BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(current_x * Constants.BLOCK_SIZE, i * Constants.BLOCK_SIZE):
                    self.fire_blocks.append(
                        init.Fire_tuple(
                            current_x * Constants.BLOCK_SIZE, i * Constants.BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(current_x * Constants.BLOCK_SIZE, i * Constants.BLOCK_SIZE):
                    self.fire_blocks.append(
                        init.Fire_tuple(
                            current_x * Constants.BLOCK_SIZE, i * Constants.BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += direction
            iteration += 1

    def get_explosion_blocks_horizontally(self, blocks_to_destroy, current_y, start_point_x, direction):
        """
        Function scanning horizontally blocks, where it should place fire animation of the bomb
        CAUTION: IT RETURNS BLOCKS AS A LIST IN THROUGH THE PARAMETER
        :param blocks_to_destroy: output list
        :param direction: -1 if left, 1 if right
        """
        i = start_point_x
        iteration = 0
        while True:
            if init.game_map[i][current_y] == Constants.STONE:
                init.game_map[i][current_y] == Constants.CLEAR
                blocks_to_destroy.append((i, current_y))
                break
            if init.game_map[i][current_y] == Constants.WALL:
                break
            if iteration > self.range_field:
                break
            if init.game_map[i][current_y] == Constants.CLEAR:
                if self.is_intersection(i * Constants.BLOCK_SIZE, current_y * Constants.BLOCK_SIZE) == True:
                    self.fire_blocks.append(
                        init.Fire_tuple(i * Constants.BLOCK_SIZE, current_y * Constants.BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(i * Constants.BLOCK_SIZE, current_y * Constants.BLOCK_SIZE):
                    self.fire_blocks.append(
                        init.Fire_tuple(i * Constants.BLOCK_SIZE, current_y * Constants.BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(i * Constants.BLOCK_SIZE, current_y * Constants.BLOCK_SIZE):
                    self.fire_blocks.append(
                       init.Fire_tuple(i * Constants.BLOCK_SIZE, current_y * Constants.BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += direction
            iteration += 1


    def get_explosion_blocks(self, blocks_to_destroy):
        """
        Function scanning vertically and horizontally blocks, where it should place fire animation of the bomb
        CAUTION: IT RETURNS BLOCKS AS A LIST IN THROUGH THE PARAMETER
        :param blocks_to_destroy: Output list
        """
        start_iter_x = (self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1
        start_iter_y = (self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1

        self.get_explosion_blocks_vertically(blocks_to_destroy, start_iter_x, start_iter_y, -1)
        self.get_explosion_blocks_vertically(blocks_to_destroy, start_iter_x, start_iter_y, 1)
        self.get_explosion_blocks_horizontally(blocks_to_destroy,  start_iter_y, start_iter_x, -1)
        self.get_explosion_blocks_horizontally(blocks_to_destroy,  start_iter_y, start_iter_x, 1)

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
                if x.direction == self.VERTICAL:
                    self.bomb_sprite.draw_vertical(
                        Constants.screen, (self.animation_step % 7) + x.block_type, x.x, x.y)
                else:
                    self.bomb_sprite.draw(
                        Constants.screen, (self.animation_step % 7) + x.block_type, x.x, x.y)
                if self.animation_step % 7 == 6:
                    if self.is_collision_with_player(playerCords):
                        health[0] -= 1
                    self.is_collision_with_ghost(ghosts)
                    self.fire_blocks.clear()
                    for x, y in self.destroyed_blocks:
                        init.game_map[x][y] = Constants.CLEAR
                    self.destroyed_blocks.clear()
                    return True
        return False

    def get_bomb_position_on_map(self):
        """
        :return: Position coordinates on map (NOT PIXELS)
        """
        x = ((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        return (x, y)

    def get_fireblocks_position(self):
        """
        :return: List of fireblocks positions
        """
        ret = []
        for x in self.fire_blocks:
            ret.append((x.x // Constants.BLOCK_SIZE, x.y // Constants.BLOCK_SIZE))
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
                        g.set_not_alive()
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
        Constants.screen.blit(self.bomb_image, (position_x, position_y))
