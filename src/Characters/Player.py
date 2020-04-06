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


    def checkExplosion(self, step):
        for item in self.BombList:
            if item.explosion(step) == True:
                self.BombList.remove(item)