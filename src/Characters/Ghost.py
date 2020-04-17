from src.Characters.Character import *
from src.Characters.Player import *
import random
class Ghost(Character):
    EASY = 11
    MEDIUM = 22
    DIFFICULT = 33

    MAX_MOVEMENT = 48
    POSSIBLE_MOVEMENTS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    distanceTraveled = 0

    def __init__(self, PositionX, PositionY, Health, Speed, BombsAmount, BombRange, ImageName):
        super(Ghost, self).__init__(PositionX, PositionY, Health,
                                    Speed, BombsAmount, BombRange, ImageName)
        self.distanceTraveled = 0
        self.currentDirection = None

    def collisionX(self, corner):
        corner += self.PositionX_change + BLOCK_SIZE
        lower_corner = self.PositionY + self.CharacterImage.get_height() + BLOCK_SIZE
        upper_corner = self.PositionY + BLOCK_SIZE
        if (game_map[corner//BLOCK_SIZE - 1][upper_corner//BLOCK_SIZE - 1] != '#' and
            game_map[corner//BLOCK_SIZE - 1][lower_corner//BLOCK_SIZE - 1] != '#'):
            self.PositionX += self.PositionX_change

    def collisionY(self, corner):
        corner += self.PositionY_change + BLOCK_SIZE
        left_corner = self.PositionX + BLOCK_SIZE
        right_corner = self.PositionX + self.CharacterImage.get_width() + BLOCK_SIZE
        if (game_map[left_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] != '#' and
            game_map[right_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] != '#'):
            self.PositionY += self.PositionY_change

    def MoveRandom(self):
        direction = random.choice(self.POSSIBLE_MOVEMENTS)
        if self.distanceTraveled == 0:
            self.currentDirection = direction
        pressed = self.currentDirection
        #print("PRESSED ", pressed)

        for key, direction in X_SPEED_CHANGE.items():
            if pressed == key:
                self.PositionX_change = direction * self.Speed
                if self.PositionX_change < 0:
                    self.collisionX(self.PositionX)
                else:
                    self.collisionX(self.PositionX + self.CharacterImage.get_width())
                self.PositionY_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed == key:
                self.PositionY_change = direction * self.Speed
                if self.PositionY_change < 0:
                    self.collisionY(self.PositionY)
                else:
                    self.collisionY(self.PositionY + self.CharacterImage.get_height())
                self.PositionY_change = 0
        self.distanceTraveled += self.Speed
        if self.distanceTraveled == self.MAX_MOVEMENT:
            self.distanceTraveled = 0
        self.setPosition(self.PositionX, self.PositionY)

    def MoveRandomWithoutBack(self):
        """
        Ghost picks random path, but cannot choose last block he was on
        """


        pass