from src.Characters.Character import *
from src.GameInitialisation import *
import time
X_SPEED_CHANGE = {
    pygame.K_LEFT: -1,
    pygame.K_RIGHT: +1,
}

Y_SPEED_CHANGE = {
    pygame.K_UP: -1,
    pygame.K_DOWN: +1,
}
# variable for tolerace setting player's possitions.
# Used in getting fireblocks collision


class Player(Character):
    PIXEL_TOLERANCE = 5
    def handleMovement(self):

        pressed = pygame.key.get_pressed()
        for key, direction in X_SPEED_CHANGE.items():
            if pressed[key]:
                self.PositionX_change = direction * self.Speed
                if self.PositionX_change < 0:
                    self.collisionX(self.PositionX)
                else:
                    self.collisionX(self.PositionX + self.CharacterImage.get_width())
                self.PositionY_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed[key]:
                self.PositionY_change = direction * self.Speed
                if self.PositionY_change < 0:
                    self.collisionY(self.PositionY)
                else:
                    self.collisionY(self.PositionY + self.CharacterImage.get_height())
                self.PositionY_change = 0
        self.setPosition(self.PositionX, self.PositionY)

    def isBombAddedToList(self):
        pressed = pygame.key.get_pressed()
        gridX = (self.PositionX + 20)//BLOCK_SIZE * BLOCK_SIZE + 3
        gridY = (self.PositionY + 20)//BLOCK_SIZE * BLOCK_SIZE + 3
        if pressed[pygame.K_SPACE]:
            if self.BombsAmount > 0:
                self.BombList.append(Bomb(gridX, gridY, self.BombRange, time.time()))
                self.BombsAmount -= 1
                return True
        return False
                

    def setBombsOnMap(self):
        if not self.BombList:
            return
        for item in self.BombList:
            if item.ShowBomb == True:
                item.setPosition(item.PositionX, item.PositionY)


    def checkExplosion(self, ghosts, playerCords):
        blocksToRemove = []
        hp = [self.Health]
        isAlive = self.IsAlive
        for item in self.BombList:
            if item.explosion(ghosts, self.getBorderPositionsOnMap(), hp, isAlive) == True:
                self.BombList.remove(item)
                self.BombsAmount += 1
                # for x, y in blocksToRemove:
                #     game_map[x][y] = ' '
                #     self.Score += 10
        self.Health = hp[0]
        if self.Health == 0:
            self.IsAlive = False

    def getPlayerPositionOnMap(self):
        x = ((self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1)
        return (x, y)

    def getBorderPositionsOnMap(self):
        pos = []
        x = ((self.PositionX + self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.PositionY + self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        pos.append((x, y))

        x = ((self.PositionX + self.CharacterImage.get_width() - self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.PositionY + self.CharacterImage.get_height() - self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        pos.append((x, y))
        return pos



