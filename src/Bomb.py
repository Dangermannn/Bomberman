from src.Characters import Character
from src.Characters import Player
from src.GameInitialisation import *
import tracemalloc
import pygame


class Bomb:
    def __init__(self, PositionX, PositionY, RangeField):
        self.PositionX = PositionX
        self.PositionY = PositionY
        self.RangeField = RangeField
        self.BombImage = pygame.image.load('Images/bomb.png')


    def explosion(self):
        for i in range(0, 3):
            self.setPosition(100, 150)
            pygame.time.wait(1000)
            self.setPosition(150, 150)
            pygame.time.wait(1000)
            
    def setPosition(self, PositionX, PositionY):
        screen.blit(self.BombImage, (PositionX, PositionY))

