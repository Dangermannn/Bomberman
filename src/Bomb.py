from src.Characters import Character
from src.Characters import Player
from src.GameInitialisation import *
from src.Tools.SpriteTool import SpriteTool
import tracemalloc
import pygame
import time

class Bomb:

    INTERSECTION = 0
    STRAIGHT = 7
    END_STRIGHT = 14
    def __init__(self, PositionX, PositionY, RangeField, SetTime):
        self.PositionX = PositionX
        self.PositionY = PositionY
        self.RangeField = RangeField
        self.BombImage = pygame.transform.scale((pygame.image.load('Images/bombv1.png').convert_alpha()), (45, 45))
        self.BombSprite = SpriteTool("Images/BombSprit.png", 7, 3, 48)
        self.FireBlocks = []
        self.SetTime = time.time()
        self.AnimationStep = 0
        self.ShowBomb = True
    def __del__(self):
        pass

    def collisionX(self, direction):
        direction += BLOCK_SIZE
        indexY = self.PositionY + BLOCK_SIZE
        if game_map[direction//BLOCK_SIZE - 1][indexY//BLOCK_SIZE - 1] == 'B':
            game_map[direction//BLOCK_SIZE - 1][indexY // BLOCK_SIZE - 1] == ' '

    def isIntersection(self, x, y):
        left = x
        right = x + 2 * BLOCK_SIZE
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        freeSides = 0
        twoFreeSides = 0
        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            freeSides += 1
        # print("LEWO", end=" ")
        if (game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            freeSides += 1
        # print("PRAWO")
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != '#'):
            freeSides += 1
        # print("GORA")
        if (game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != '#'):
            freeSides += 1

        # print("DOL")
        # print("LEFT: ", left // BLOCK_SIZE - 1, " ", y // BLOCK_SIZE - 1, " RIGHT = ", right // BLOCK_SIZE - 1)
        # pritn("UP: ", coorinates[0]//BLOCK_SIZE - 1, " ", up // BLOCK_SIZE - 1, ' DOWN = ', down // BLOCK_SIZE - 1 )
        if freeSides >= 3:
            print("THREE SIDES")
            return True
        return False


    def isVertical(self, x, y):
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        print("down = ", down // BLOCK_SIZE, " up = ", up // BLOCK_SIZE)
        # print("left = ", x // BLOCK_SIZE)
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != '#') and (
                game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != '#'):
            return True
        return False

    def isHorizontal(self, x, y):
        left = x
        right = x + 2 * BLOCK_SIZE
        # print("LEFT POS = ", left, " RIGHT POS = ", right)
        # print("LEFT = ", left//BLOCK_SIZE - 1, " RIGHT = ", right // BLOCK_SIZE - 1, " Y = ", y // BLOCK_SIZE - 1)
        # print(y // BLOCK_SIZE)
        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#') and (
                game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            return True
        return False

    def explosionBlocks(self):
        currentX = (self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1
        i = (self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1
        print("BOMB 1 POS X = ", self.PositionX, " POS Y = ", self.PositionY, " X = " , currentX, " Y = ", i)
        # vertical
        while True:
            print("GAME_MAP = ", " currentX = ", currentX, " i = ", i, game_map[currentX][i])
            if game_map[currentX][i] == 'S':
                game_map[currentX][i] == ' '
                break
            if game_map[currentX][i] == '#':
                break;
            if game_map[currentX][i] == ' ':
                if self.isIntersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    print(self.isIntersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE))
                    print("IS INTERSECTION")
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION))
                elif self.isVertical(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT))
                elif self.isHorizontal(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT))
            i += 1


        i = (self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 2
        while game_map[currentX][i] == ' ':
            if game_map[currentX][i] == ' ':
                if self.isIntersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE) == True:
                    print("IS INTERSECTION")
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION))
                elif self.isVertical(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT))
                elif self.isHorizontal(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT))
            i -= 1

    def fire(self):
        for x in self.FireBlocks:
            print(x)
            
    def explosion(self, step):
        
        self.explosionBlocks()
        t = time.time()
        if t - self.SetTime > 2:
            self.ShowBomb = False
            self.AnimationStep += 1
            for x in self.FireBlocks:
                #self.BombSprite.draw(screen, (step % 7) + x[2], x[0], x[1])
                self.BombSprite.draw(screen, (self.AnimationStep % 7) + x[2], x[0], x[1])
                #pygame.time.wait(2)
                #if step % 7 == 6:
                if self.AnimationStep % 7 == 6:
                    print("6666666666666666")
                    self.FireBlocks.clear()
                    return True
        return False

    def setPosition(self, PositionX, PositionY):
        screen.blit(self.BombImage, (PositionX, PositionY))

    def removeBomb(self):
        del self
