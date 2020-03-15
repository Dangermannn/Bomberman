import pygame
import os
from src.Bomb import Bomb
from src.GameInitialisation import *
from pygame import Surface


class Character:  

    def __init__(self, PositionX, PositionY, Health, Speed, BombsAmount, BombRange, ImageName):
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
        self.Score = 0
        self.IsAlive = True

    def getInfo(self):
        print(self.PositionX, "\t", self.PositionY, "\t", self.PositionX_change, self.PositionY_change)

    def setPosition(self, PositionX, PositionY):
        screen.blit(self.CharacterImage, (PositionX, PositionY))

    