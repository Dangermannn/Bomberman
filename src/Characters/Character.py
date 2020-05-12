import pygame
import os
from src.Bomb import Bomb
from src.GameInitialisation import *
from pygame import Surface


class Character:  
    FREE_WAY = [' ', 'P']

    def __init__(self, position_x = 50, position_y = 50, health = 5, speed = 6,
                 bomb_amount = 13, bomb_range = 13, image_name = "Images/Hero.png"):
        self.position_x = position_x
        self.position_y = position_y
        self.health = health
        self.speed = speed
        self.bomb_amount = bomb_amount
        self.bomb_range = bomb_range
        self.position_x_change = 0
        self.position_y_change = 0
        self.bomb_list = []
        self.character_image = pygame.transform.scale((pygame.image.load(image_name).convert_alpha()), (40, 40))
        self.is_alive = True
        self.default_position = (position_x, position_x)
        self.last_position = (1, 1)

    def set_to_default(self):
        """
        Setting character stats to default
        """
        self.position_x = 50
        self.position_y = 50
        self.position_x_change = 0
        self.position_y_change = 0
        self.bomb_list = []
        #self.Score = 0
        self.is_alive = True

    def collision_x(self, corner):
        """
        Function for checking collision on x-coordinate. If there's no collision, player moves.
        :param corner: player's corner position
        """
        corner += self.position_x_change + BLOCK_SIZE
        lower_corner = self.position_y + self.character_image.get_height() + BLOCK_SIZE
        upper_corner = self.position_y + BLOCK_SIZE
        if (game_map[corner//BLOCK_SIZE - 1][upper_corner//BLOCK_SIZE - 1] in self.FREE_WAY and
            game_map[corner//BLOCK_SIZE - 1][lower_corner//BLOCK_SIZE - 1] in self.FREE_WAY):
            self.position_x += self.position_x_change

    def collision_y(self, corner):
        """
        Function for checking collision on x-coordinate. If there's no collision, player moves.
        :param corner: player's corner position
        """
        corner += self.position_y_change + BLOCK_SIZE
        left_corner = self.position_x + BLOCK_SIZE
        right_corner = self.position_x + self.character_image.get_width() + BLOCK_SIZE
        if (game_map[left_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] in self.FREE_WAY and
            game_map[right_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] in self.FREE_WAY):
            self.position_y += self.position_y_change

    def set_position(self, position_x, position_y):
        """
        Placing bot on map
        :param position_x: character's position
        :param position_y: character's position
        """
        screen.blit(self.character_image, (position_x, position_y))
