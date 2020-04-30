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
    VERTICAL = 1
    HORIZONTAL = 2
    def __init__(self, PositionX, PositionY, RangeField, SetTime):
        self.PositionX = PositionX
        self.PositionY = PositionY
        self.RangeField = RangeField
        self.BombImage = pygame.transform.scale((pygame.image.load('Images/bombv1.png').convert_alpha()), (45, 45))
        self.BombSprite = SpriteTool("Images/BombSprit.png", 7, 3, 48)
        self.FireBlocks = []
        self.DestroyedBlocks = []
        self.SetTime = time.time()
        self.AnimationStep = 0
        self.LastAnimationTime = time.time()
        self.ShowBomb = True

    def __del__(self):
        pass

    def collisionX(self, direction):
        direction += BLOCK_SIZE
        indexY = self.PositionY + BLOCK_SIZE
        if game_map[direction // BLOCK_SIZE - 1][indexY // BLOCK_SIZE - 1] == 'B':
            game_map[direction // BLOCK_SIZE - 1][indexY // BLOCK_SIZE - 1] == ' '


    def isIntersection(self, x, y):
        left = x
        right = x + 2 * BLOCK_SIZE
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        freeSides = 0
        leftSide = False
        rightSide = False
        upperSide = False
        downSide = False
        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            leftSide = True
            freeSides += 1
        # print("LEWO", end=" ")
        if (game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            rightSide = True
            freeSides += 1
        # print("PRAWO")
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != '#'):
            upperSide = True
            freeSides += 1
        # print("GORA")
        if (game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != '#'):
            downSide = True
            freeSides += 1

        if freeSides >= 3:
            return True
        elif (leftSide and  (upperSide or downSide))  or (rightSide and (upperSide or downSide)):
            return True
        return False

    def isVertical(self, x, y):
        down = y + BLOCK_SIZE
        up = y - BLOCK_SIZE
        if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != '#') or (
                game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != '#'):
            return True
        return False

    def isHorizontal(self, x, y):
        left = x
        right = x + 2 * BLOCK_SIZE

        if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#') or (
                game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
            return True
        return False

    def explosionBlocks(self, sHit):
        iteration = 0
        currentX = (self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1
        i = (self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1

        # downward
        while True:
            if game_map[currentX][i] == 'S':
                game_map[currentX][i] == ' '
                sHit.append((currentX, i))
                break
            if game_map[currentX][i] == '#':
                break;
            if iteration > self.RangeField:
                break
            if game_map[currentX][i] == ' ':
                if self.isIntersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    print(self.isIntersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE))
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.isVertical(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.isHorizontal(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += 1
            iteration += 1

        iteration = 0
        i = (self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1
        # upward
        while True:
            if game_map[currentX][i] == 'S':
                game_map[currentX][i] == ' '
                sHit.append((currentX, i))
                break
            if game_map[currentX][i] == '#':
                break
            if iteration > self.RangeField:
                break
            if game_map[currentX][i] == ' ':
                if self.isIntersection(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.isVertical(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.isHorizontal(currentX * BLOCK_SIZE, i * BLOCK_SIZE):
                    self.FireBlocks.append((currentX * BLOCK_SIZE, i * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i -= 1
            iteration += 1

        iteration = 0
        currentY = (self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1
        i = (self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1
        # print(" -------------- LEFT ----------------------")
        while True:
            if game_map[i][currentY] == 'S':
                game_map[i][currentY] == ' '
                sHit.append((i, currentY))
                break
            if game_map[i][currentY] == '#':
                break
            if iteration > self.RangeField:
                break
            if game_map[i][currentY] == ' ':
                if self.isIntersection(i * BLOCK_SIZE, currentY * BLOCK_SIZE) == True:
                    self.FireBlocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.isVertical(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.FireBlocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.isHorizontal(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.FireBlocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i -= 1
            iteration += 1

        iteration = 0
        i = (self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1

        while True:

            if game_map[i][currentY] == 'S':
                game_map[i][currentY] == ' '
                sHit.append((i, currentY))
                break
            if game_map[i][currentY] == '#':
                break
            if iteration > self.RangeField:
                break
            if game_map[i][currentY] == ' ':
                if self.isIntersection(i * BLOCK_SIZE, currentY * BLOCK_SIZE) == True:
                    self.FireBlocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.INTERSECTION, None))
                elif self.isVertical(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.FireBlocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.VERTICAL))
                elif self.isHorizontal(i * BLOCK_SIZE, currentY * BLOCK_SIZE):
                    self.FireBlocks.append((i * BLOCK_SIZE, currentY * BLOCK_SIZE, self.STRAIGHT, self.HORIZONTAL))
            i += 1
            iteration += 1

    def explosion(self, destroyedBlocks, ghosts, playerCords, health, isAlive):
        if self.AnimationStep == 0:
            self.explosionBlocks(self.DestroyedBlocks)
        explosionTimer = time.time()
        if explosionTimer - self.SetTime > 2:
            self.ShowBomb = False
            if time.time() - self.LastAnimationTime > 0.05:
                self.AnimationStep += 1
                self.LastAnimationTime = time.time()
            for x in self.FireBlocks:
                if x[3] == self.VERTICAL:
                    self.BombSprite.drawVertical(screen, (self.AnimationStep % 7) + x[2], x[0], x[1])
                else:
                    self.BombSprite.draw(screen, (self.AnimationStep % 7) + x[2], x[0], x[1])
                if self.AnimationStep % 7 == 6:
                    if self.isCollisionWithPlayer(playerCords):
                        health[0] -= 1
                    self.isCollisionWithGhost(ghosts)
                    self.FireBlocks.clear()
                    for x, y in self.DestroyedBlocks:
                        game_map[x][y] = ' '
                    self.DestroyedBlocks.clear()
                    return True
        return False

    def getBombPositionOnMap(self):
        x = ((self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1)
        return (x, y)

    def getFireBlocksPosition(self):
        ret = []
        for x in self.FireBlocks:
            ret.append((x[0] // BLOCK_SIZE, x[1] // BLOCK_SIZE))
        return ret

    def isCollisionWithGhost(self, ghosts):
        blocks = self.getFireBlocksPosition()
        for b in blocks:
            for g in ghosts:
                if g.getPositionOnMap() == b:
                    g.Health -= 1
                    if g.Health == 0:
                        g.isAlive = False
                        ghosts.remove(g)

    def isCollisionWithPlayer(self, coords):
        blocks = self.getFireBlocksPosition()
        for b in blocks:
            if b == coords:
                return True
        return False

    def setPosition(self, PositionX, PositionY):
        screen.blit(self.BombImage, (PositionX, PositionY))

    def removeBomb(self):
        del self
