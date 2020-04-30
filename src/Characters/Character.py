import pygame
import os
from src.Bomb import Bomb
from src.GameInitialisation import *
from pygame import Surface


class Character:  

    def __init__(self, PositionX = 50, PositionY = 50, Health = 5, Speed = 6,
                 BombsAmount = 13, BombRange = 13, ImageName = "Images/Hero.png"):
        self.PositionX = PositionX
        self.PositionY = PositionY
        self.Health = Health
        self.Speed = Speed
        self.BombsAmount = BombsAmount
        self.BombRange = BombRange
        self.PositionX_change = 0
        self.PositionY_change = 0
        self.BombList = []
        self.CharacterImage = pygame.transform.scale((pygame.image.load(ImageName).convert_alpha()), (40, 40))
        self.IsAlive = True
        self.DefaultPosition = (PositionX, PositionX)

    def setToDefault(self):
        self.PositionX = 50
        self.PositionY = 50
        self.PositionX_change = 0
        self.PositionY_change = 0
        self.BombList = []
        self.Score = 0
        self.IsAlive = True


    def getInfo(self):
        print(self.PositionX, "\t", self.PositionY, "\t", self.PositionX_change, self.PositionY_change)

    def collisionX(self, corner):
        corner += self.PositionX_change + BLOCK_SIZE
        lower_corner = self.PositionY + self.CharacterImage.get_height() + BLOCK_SIZE
        upper_corner = self.PositionY + BLOCK_SIZE
        if (game_map[corner//BLOCK_SIZE - 1][upper_corner//BLOCK_SIZE - 1] == ' ' and
            game_map[corner//BLOCK_SIZE - 1][lower_corner//BLOCK_SIZE - 1] == ' '):
            self.PositionX += self.PositionX_change

    def collisionY(self, corner):
        corner += self.PositionY_change + BLOCK_SIZE
        left_corner = self.PositionX + BLOCK_SIZE
        right_corner = self.PositionX + self.CharacterImage.get_width() + BLOCK_SIZE
        if (game_map[left_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] == ' ' and
            game_map[right_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] == ' '):
            self.PositionY += self.PositionY_change

    def setPosition(self, PositionX, PositionY):
        screen.blit(self.CharacterImage, (PositionX, PositionY))
