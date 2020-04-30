from src.Characters.Character import *
from src.Characters.Player import *
from src.GameInitialisation import *
import random
class Ghost(Character):
    EASY = 1
    MEDIUM = 2
    MAX_MOVEMENT = 50
    POSSIBLE_MOVEMENTS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    def __init__(self, PositionX, PositionY, Health, Speed, BombsAmount, BombRange, ImageName, Mode):
        super(Ghost, self).__init__(PositionX, PositionY, Health,
                                    Speed, BombsAmount, BombRange, ImageName)
        self.CharacterImage = pygame.transform.scale((pygame.image.load(ImageName).convert_alpha()), (44, 44))
        self.distanceTraveled = 0
        self.currentDirection = None
        self.possibleMovements = []
        self.lastPositions = []
        self.lastPositions.append((((self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1),
                                      ((self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1)))
        self.isAlive = True
        self.Mode = Mode
        self.DefaultPosition = (PositionX, PositionY)

    def setToDefault(self):
        self.PositionX = self.DefaultPosition[0]
        self.PositionY = self.DefaultPosition[1]
        self.Health = 1
        self.isAlive = True

    def collisionX(self, corner):
        corner += self.PositionX_change + BLOCK_SIZE
        lower_corner = self.PositionY + self.CharacterImage.get_height() + BLOCK_SIZE
        upper_corner = self.PositionY + BLOCK_SIZE
        if (game_map[corner//BLOCK_SIZE - 1][upper_corner//BLOCK_SIZE - 1] != '#' and
            game_map[corner//BLOCK_SIZE - 1][lower_corner//BLOCK_SIZE - 1] != '#'):
            if self.distanceTraveled < self.MAX_MOVEMENT:
                self.PositionX += self.PositionX_change
            else:
                self.PositionX += (self.MAX_MOVEMENT - self.distanceTraveled)
                self.distanceTraveled = 0
                #print("======================", self.PositionX, " ", self.PositionY, "======================")

        #distanceToBoundary = (self.PositionX // BLOCK_SIZE + 1) * BLOCK_SIZE - self.PositionX
        #print("DISTANCE TO X: ", distanceToBoundary)
        #if distanceToBoundary <= self.Speed:
           # self.PositionX += distanceToBoundary

    def collisionY(self, corner):
        corner += self.PositionY_change + BLOCK_SIZE
        left_corner = self.PositionX + BLOCK_SIZE
        right_corner = self.PositionX + self.CharacterImage.get_width() + BLOCK_SIZE
        if (game_map[left_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] != '#' and
            game_map[right_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] != '#'):
            if self.distanceTraveled < self.MAX_MOVEMENT:
                self.PositionY += self.PositionY_change
            else:
                self.PositionY += (self.MAX_MOVEMENT - self.distanceTraveled)
                self.distanceTraveled = 0
                #print("======================", self.PositionX, " ", self.PositionY, "======================")

        #distanceToBoundary = (self.PositionX // BLOCK_SIZE + 1) * BLOCK_SIZE - self.PositionX
        #print("DISTANCE TO Y: ", distanceToBoundary)
        #if distanceToBoundary <= self.Speed:
          #  self.PositionX += distanceToBoundary

    def moveRandom(self):

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
        if self.distanceTraveled >= self.MAX_MOVEMENT:
            self.distanceTraveled = 0
        self.setPosition(self.PositionX, self.PositionY)

    def moveRandomWithoutBack(self):
        """
        Ghost picks random path, but cannot choose last block he was on
        """
        x = ((self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = ((self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
        if self.distanceTraveled == 0:
            x = ((self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
            y = ((self.PositionY  + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
            # available paths
            left = x
            right = x + 2 * BLOCK_SIZE
            down = y + BLOCK_SIZE
            up = y - BLOCK_SIZE
            leftSide = False
            rightSide = False
            upperSide = False
            downSide = False
            print("-------------------------------------------------------------------")
            print("DISTANCE TRAVELED", self.distanceTraveled)
            print("WARUNKI")
            print("POSITION: [", x // BLOCK_SIZE, ", ", y // BLOCK_SIZE, "]")
            #print("LEFT: [", left // BLOCK_SIZE - 1, ", ", y // BLOCK_SIZE, "]", "GAME MAP: ", game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] )
            if (game_map[left // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
                leftSide = True
            if (game_map[right // BLOCK_SIZE - 1][y // BLOCK_SIZE] != '#'):
                rightSide = True
            if (game_map[x // BLOCK_SIZE][up // BLOCK_SIZE] != '#'):
                upperSide = True
            if (game_map[x // BLOCK_SIZE][down // BLOCK_SIZE] != '#'):
                downSide = True


            print("LAST POSITIONS: ", self.lastPositions)
           # print("LEWO: ", leftSide, " PRAWO: ", rightSide, " GORA", upperSide, " DOL", downSide)
            print("UPPER: ", (x // BLOCK_SIZE, y // BLOCK_SIZE - 1))
            print("LEFT: ", (x // BLOCK_SIZE - 1, y // BLOCK_SIZE))
            print("RIGHT: ", (x // BLOCK_SIZE + 1, y // BLOCK_SIZE))
            print("DOWN: ", (x // BLOCK_SIZE, y // BLOCK_SIZE + 1))
            if (upperSide and (x//BLOCK_SIZE, y // BLOCK_SIZE - 1) not in self.lastPositions) or (y // BLOCK_SIZE - 1 == 12):
                self.possibleMovements.append(self.POSSIBLE_MOVEMENTS[2])
               # print("APPENDED x, y : [",x // BLOCK_SIZE, ", ", y // BLOCK_SIZE - 1, "]")
                print("DODAJTE GORA")
            if (leftSide and (x // BLOCK_SIZE - 1, y // BLOCK_SIZE) not in self.lastPositions) or (x // BLOCK_SIZE - 1 == 12):
                self.possibleMovements.append(self.POSSIBLE_MOVEMENTS[0])
               # print("APPENDED x, y : [",x // BLOCK_SIZE - 1, ", ", y // BLOCK_SIZE, "]")
                print("DODAJE LEWO")
            if (rightSide and (x // BLOCK_SIZE + 1, y // BLOCK_SIZE) not in self.lastPositions) or (x // BLOCK_SIZE + 1 == 2):
                self.possibleMovements.append(self.POSSIBLE_MOVEMENTS[1])
                print("DODAJE PRAWO")
            if (downSide and (x // BLOCK_SIZE, y // BLOCK_SIZE + 1) not in self.lastPositions) or (y // BLOCK_SIZE + 1 == 2):
                self.possibleMovements.append(self.POSSIBLE_MOVEMENTS[3])
                print("DODAJE DOL")

        #self.setPosition(self.PositionX, self.PositionY)

        if not self.possibleMovements:
            self.possibleMovements.append(None)

        if len(self.lastPositions) == 6:
            self.lastPositions.pop(0)

        if self.distanceTraveled == 0:
            direction = random.choice(self.possibleMovements)

        if self.distanceTraveled == 0:
            self.currentDirection = direction
        pressed = self.currentDirection
        # print("PRESSED ", pressed)

        for key, direction in X_SPEED_CHANGE.items():
            if pressed == key:
                self.PositionX_change = direction * self.Speed
                if self.PositionX_change < 0:
                    self.collisionX(self.PositionX)
                    if self.distanceTraveled == 0:
                        self.lastPositions.append((x // BLOCK_SIZE, y // BLOCK_SIZE))
                        print("LEFT ADDED: [", x//BLOCK_SIZE, ", ", y//BLOCK_SIZE, "]")
                else:
                    self.collisionX(self.PositionX + self.CharacterImage.get_width())
                    if self.distanceTraveled == 0:
                        self.lastPositions.append((x // BLOCK_SIZE, y // BLOCK_SIZE))
                        print("RIGHT ADDED: [", x // BLOCK_SIZE, ", ", y // BLOCK_SIZE, "]")
                self.PositionY_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed == key:
                self.PositionY_change = direction * self.Speed
                if self.PositionY_change < 0:
                    self.collisionY(self.PositionY)
                    if self.distanceTraveled == 0:
                        self.lastPositions.append((x // BLOCK_SIZE, y // BLOCK_SIZE ))
                        print("UP ADDED: [", x // BLOCK_SIZE, ", ", y // BLOCK_SIZE, "]")
                else:
                    self.collisionY(self.PositionY + self.CharacterImage.get_height())
                    if self.distanceTraveled == 0:
                        self.lastPositions.append((x // BLOCK_SIZE, y // BLOCK_SIZE))
                        print("LEFT ADDED: [", x // BLOCK_SIZE, ", ", y // BLOCK_SIZE, "]")
                self.PositionY_change = 0
        self.distanceTraveled += self.Speed
        #print("DISTANCE AFTER ADDING", self.distanceTraveled)
        if self.distanceTraveled >= self.MAX_MOVEMENT:
            self.distanceTraveled = 0
        self.setPosition(self.PositionX, self.PositionY)

        self.possibleMovements.clear()

    def getPositionOnMap(self):
        x = ((self.PositionX + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.PositionY + BLOCK_SIZE) // BLOCK_SIZE - 1)
        return (x, y)

    def handleMovement(self):
        if self.Mode == self.EASY and self.isAlive == True:
            self.moveRandom()
        elif self.Mode == self.MEDIUM and self.isAlive == True:
            self.moveRandomWithoutBack()


    def removeGhost(self):
        del self