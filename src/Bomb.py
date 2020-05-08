from src.Characters import Character
from src.Characters import Player
from src.GameInitialisation import *
from src.Tools.SpriteTool import SpriteTool
from pygame import mixer
import tracemalloc
import pygame
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
        self.bomb_image = pygame.transform.scale((pygame.image.load('Images/bombv1.png').convert_alpha()), (45, 45))
        self.bomb_sprite = SpriteTool("Images/BombSprit.png", 7, 3, 48)
        self.fire_blocks = []
        self.destroyed_blocks = []
        self.set_time = time.time()
        self.animation_step = 0
        self.last_animation_time = time.time()
        self.show_bomb = True
        self.explosion_sound = mixer.Sound('Sounds/bombExplosion.wav')

    def __del__(self):
        pass

    def is_intersection(self, x, y):
        left = x
        right = x + 2 * BLOCK_SIZE
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        free_sized = 0
        left_size = False
        right_side = False
        upper_size = False
        down_side = False
        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            left_size = True
            free_sized += 1
        # print("LEWO", end=" ")
        if (game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            right_side = True
            free_sized += 1
        # print("PRAWO")
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != '#'):
            upper_size = True
            free_sized += 1
        # print("GORA")
        if (game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != '#'):
            down_side = True
            free_sized += 1

        if free_sized >= 3:
            return True
        elif (left_size and  (upper_size or down_side))  or (right_side and (upper_size or down_side)):
            return True
        return False

    def is_vertical(self, x, y):
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != '#') or (
                game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != '#'):
            return True
        return False

    def is_horizontal(self, x, y):
        left = x
        right = x + 2 * BLOCK_SIZE

        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#') or (
                game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            return True
        return False

    def get_explosion_blocks(self, sHit):
        iteration = 0
        currentX = (self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1
        i = (self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1

        # downward
        while True:
            if game_map[currentX][i] == 'S':
                game_map[currentX][i] == ' '
                sHit.append((currentX, i))
                break
            if game_map[currentX][i] == '#':
                break;
            if iteration > self.range_field:
                break
            if game_map[currentX][i] == ' ':
                if self.is_intersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += 1
            iteration += 1

        iteration = 0
        i = (self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1
        # upward
        while True:
            if game_map[currentX][i] == 'S':
                game_map[currentX][i] == ' '
                sHit.append((currentX, i))
                break
            if game_map[currentX][i] == '#':
                break
            if iteration > self.range_field:
                break
            if game_map[currentX][i] == ' ':
                if self.is_intersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.fire_blocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i -= 1
            iteration += 1

        iteration = 0
        currentY = (self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1
        i = (self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1
        # print(" -------------- LEFT ----------------------")
        while True:
            if game_map[i][currentY] == 'S':
                game_map[i][currentY] == ' '
                sHit.append((i, currentY))
                break
            if game_map[i][currentY] == '#':
                break
            if iteration > self.range_field:
                break
            if game_map[i][currentY] == ' ':
                if self.is_intersection(i * BLOCK_SIZE, currentY * BLOCK_SIZE) == True:
                    self.fire_blocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i -= 1
            iteration += 1

        iteration = 0
        i = (self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1
        # -------------- DOWNWARD -------------
        while True:

            if game_map[i][currentY] == 'S':
                game_map[i][currentY] == ' '
                sHit.append((i, currentY))
                break
            if game_map[i][currentY] == '#':
                break
            if iteration > self.range_field:
                break
            if game_map[i][currentY] == ' ':
                if self.is_intersection(i * BLOCK_SIZE, currentY * BLOCK_SIZE) == True:
                    self.fire_blocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.is_vertical(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.is_horizontal(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.fire_blocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += 1
            iteration += 1

    def explosion(self, ghosts, playerCords, health, is_alive):
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
                    self.bomb_sprite.drawVertical(screen, (self.animation_step % 7) + x[2], x[0], x[1])
                else:
                    self.bomb_sprite.draw(screen, (self.animation_step % 7) + x[2], x[0], x[1])
                if self.animation_step % 7 == 6:
                    if self.is_collision_with_player(playerCords):
                        health[0] -= 1
                    self.is_collision_with_ghost(ghosts)
                    self.fire_blocks.clear()
                    for x, y in self.destroyed_blocks:
                        game_map[x][y] = ' '
                    self.destroyed_blocks.clear()
                    return True
        return False

    def get_bomb_position_on_map(self):
        x = ((self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1)
        return (x, y)

    def get_fireblocks_position(self):
        ret = []
        for x in self.fire_blocks:
            ret.append((x[0] // BLOCK_SIZE, x[1] // BLOCK_SIZE))
        return ret

    def is_collision_with_ghost(self, ghosts):
        blocks = self.get_fireblocks_position()
        for b in blocks:
            for g in ghosts:
                pos = []
                pos = g.get_border_positions_on_map()
                for p in pos:
                    if p == b:
                        g.health -= 1
                        if g.health == 0:
                            g.is_alive = False
                            ghosts.remove(g)

    def is_collision_with_player(self, coords):
        blocks = self.get_fireblocks_position()
        for b in blocks:
            for c in coords:
                if c == b:
                    return True
        return False

    def set_position(self, position_x, position_y):
        screen.blit(self.bomb_image, (position_x, position_y))

    def remove_bomb(self):
        del self
