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



class Player(Character):

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
        #map(lambda x: x.setPosition(self.PositionX, self.PositionY), self.BombList)
        if not self.BombList:
            return
        for item in self.BombList:
            if item.ShowBomb == True:
                item.setPosition(item.PositionX, item.PositionY)


    def checkExplosion(self):
        array = []
        for item in self.BombList:
            if item.explosion(array) == True:
                self.BombList.remove(item)
                self.BombsAmount += 1
                for x, y in array:
                    game_map[x][y] = ' '
                    self.Score += 10