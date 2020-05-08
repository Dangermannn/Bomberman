from src.Characters.Character import *
from src.Characters.Player import *
from src.GameInitialisation import *
import random
class Ghost(Character):
    EASY = 1
    MEDIUM = 2
    MAX_MOVEMENT = 50

    PIXEL_TOLERANCE = 3

    POSSIBLE_MOVEMENTS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    def __init__(self, position_x, position_y, health, speed, bomb_amount, bomb_range, image_name, mode):
        super(Ghost, self).__init__(position_x, position_y, health,
                                    speed, bomb_amount, bomb_range, image_name)
        self.character_image = pygame.transform.scale((pygame.image.load(image_name).convert_alpha()), (44, 44))
        self.distance_traveled = 0
        self.current_direction = None
        self.possible_movements = []
        self.last_positions = []
        self.last_positions.append((((self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1),
                                      ((self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1)))
        self.is_alive = True
        self.mode = mode
        self.default_position = (position_x, position_y)

    def set_to_default(self):
        self.position_x = self.default_position[0]
        self.position_y = self.default_position[1]
        self.health = 1
        self.is_alive = True

    def collision_x(self, corner):
        corner += self.position_x_change + BLOCK_SIZE
        lower_corner = self.position_y + self.character_image.get_height() + BLOCK_SIZE
        upper_corner = self.position_y + BLOCK_SIZE
        if (game_map[corner//BLOCK_SIZE - 1][upper_corner//BLOCK_SIZE - 1] != '#' and
            game_map[corner//BLOCK_SIZE - 1][lower_corner//BLOCK_SIZE - 1] != '#'):
            if self.distance_traveled < self.MAX_MOVEMENT:
                self.position_x += self.position_x_change
            else:
                self.position_x += (self.MAX_MOVEMENT - self.distance_traveled)
                self.distance_traveled = 0
                #print("======================", self.PositionX, " ", self.PositionY, "======================")

        #distanceToBoundary = (self.PositionX // BLOCK_SIZE + 1) * BLOCK_SIZE - self.PositionX
        #print("DISTANCE TO X: ", distanceToBoundary)
        #if distanceToBoundary <= self.Speed:
           # self.PositionX += distanceToBoundary

    def collision_y(self, corner):
        corner += self.position_y_change + BLOCK_SIZE
        left_corner = self.position_x + BLOCK_SIZE
        right_corner = self.position_x + self.character_image.get_width() + BLOCK_SIZE
        if (game_map[left_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] != '#' and
            game_map[right_corner//BLOCK_SIZE - 1][corner//BLOCK_SIZE - 1] != '#'):
            if self.distance_traveled < self.MAX_MOVEMENT:
                self.position_y += self.position_y_change
            else:
                self.position_y += (self.MAX_MOVEMENT - self.distance_traveled)
                self.distance_traveled = 0
                #print("======================", self.PositionX, " ", self.PositionY, "======================")

        #distanceToBoundary = (self.PositionX // BLOCK_SIZE + 1) * BLOCK_SIZE - self.PositionX
        #print("DISTANCE TO Y: ", distanceToBoundary)
        #if distanceToBoundary <= self.Speed:
          #  self.PositionX += distanceToBoundary

    def moveRandom(self):

        direction = random.choice(self.POSSIBLE_MOVEMENTS)
        if self.distance_traveled == 0:
            self.current_direction = direction
        pressed = self.current_direction
        #print("PRESSED ", pressed)

        for key, direction in X_SPEED_CHANGE.items():
            if pressed == key:
                self.position_x_change = direction * self.speed
                if self.position_x_change < 0:
                    self.collision_x(self.position_x)
                else:
                    self.collision_x(self.position_x + self.character_image.get_width())
                self.position_y_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed == key:
                self.position_y_change = direction * self.speed
                if self.position_y_change < 0:
                    self.collision_y(self.position_y)
                else:
                    self.collision_y(self.position_y + self.character_image.get_height())
                self.position_y_change = 0
        self.distance_traveled += self.speed
        if self.distance_traveled >= self.MAX_MOVEMENT:
            self.distance_traveled = 0
        self.set_position(self.position_x, self.position_y)

    def moveRandomWithoutBack(self):
        """
        Ghost picks random path, but cannot choose last block he was on
        """
        x = ((self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = ((self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
        if self.distance_traveled == 0:
            x = ((self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
            y = ((self.position_y  + BLOCK_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
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
            print("DISTANCE TRAVELED", self.distance_traveled)
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


            print("LAST POSITIONS: ", self.last_positions)
           # print("LEWO: ", leftSide, " PRAWO: ", rightSide, " GORA", upperSide, " DOL", downSide)
            print("UPPER: ", (x // BLOCK_SIZE, y // BLOCK_SIZE - 1))
            print("LEFT: ", (x // BLOCK_SIZE - 1, y // BLOCK_SIZE))
            print("RIGHT: ", (x // BLOCK_SIZE + 1, y // BLOCK_SIZE))
            print("DOWN: ", (x // BLOCK_SIZE, y // BLOCK_SIZE + 1))
            if (upperSide and (x//BLOCK_SIZE, y // BLOCK_SIZE - 1) not in self.last_positions) or (y // BLOCK_SIZE - 1 == 12):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[2])
               # print("APPENDED x, y : [",x // BLOCK_SIZE, ", ", y // BLOCK_SIZE - 1, "]")
                print("DODAJTE GORA")
            if (leftSide and (x // BLOCK_SIZE - 1, y // BLOCK_SIZE) not in self.last_positions) or (x // BLOCK_SIZE - 1 == 12):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[0])
               # print("APPENDED x, y : [",x // BLOCK_SIZE - 1, ", ", y // BLOCK_SIZE, "]")
                print("DODAJE LEWO")
            if (rightSide and (x // BLOCK_SIZE + 1, y // BLOCK_SIZE) not in self.last_positions) or (x // BLOCK_SIZE + 1 == 2):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[1])
                print("DODAJE PRAWO")
            if (downSide and (x // BLOCK_SIZE, y // BLOCK_SIZE + 1) not in self.last_positions) or (y // BLOCK_SIZE + 1 == 2):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[3])
                print("DODAJE DOL")
        print("DISTANCE: ", self.distance_traveled)
        #self.setPosition(self.PositionX, self.PositionY)

        if not self.possible_movements:
            self.possible_movements.append(None)

        if len(self.last_positions) == 6:
            self.last_positions.pop(0)

        if self.distance_traveled == 0:
            direction = random.choice(self.possible_movements)

        if self.distance_traveled == 0:
            self.current_direction = direction
        pressed = self.current_direction
        # print("PRESSED ", pressed)

        for key, direction in X_SPEED_CHANGE.items():
            if pressed == key:
                self.position_x_change = direction * self.speed
                if self.position_x_change < 0:
                    self.collision_x(self.position_x)
                    if self.distance_traveled == 0:
                        self.last_positions.append((x // BLOCK_SIZE, y // BLOCK_SIZE))
                        print("LEFT ADDED: [", x//BLOCK_SIZE, ", ", y//BLOCK_SIZE, "]")
                else:
                    self.collision_x(self.position_x + self.character_image.get_width())
                    if self.distance_traveled == 0:
                        self.last_positions.append((x // BLOCK_SIZE, y // BLOCK_SIZE))
                        print("RIGHT ADDED: [", x // BLOCK_SIZE, ", ", y // BLOCK_SIZE, "]")
                self.position_y_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed == key:
                self.position_y_change = direction * self.speed
                if self.position_y_change < 0:
                    self.collision_y(self.position_y)
                    if self.distance_traveled == 0:
                        self.last_positions.append((x // BLOCK_SIZE, y // BLOCK_SIZE ))
                        print("UP ADDED: [", x // BLOCK_SIZE, ", ", y // BLOCK_SIZE, "]")
                else:
                    self.collision_y(self.position_y + self.character_image.get_height())
                    if self.distance_traveled == 0:
                        self.last_positions.append((x // BLOCK_SIZE, y // BLOCK_SIZE))
                        print("LEFT ADDED: [", x // BLOCK_SIZE, ", ", y // BLOCK_SIZE, "]")
                self.position_y_change = 0
        self.distance_traveled += self.speed
        #print("DISTANCE AFTER ADDING", self.distanceTraveled)
        if self.distance_traveled >= self.MAX_MOVEMENT:
            self.distance_traveled = 0
        self.set_position(self.position_x, self.position_y)

        self.possible_movements.clear()

    def get_position_on_map(self):
        x = ((self.position_x + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.position_y + BLOCK_SIZE) // BLOCK_SIZE - 1)
        return (x, y)

    def get_border_positions_on_map(self):
        pos = []
        x = ((self.position_x + self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.position_y + self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        pos.append((x, y))

        x = ((self.position_x + self.character_image.get_width() - self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        y = ((self.position_y + self.character_image.get_height() - self.PIXEL_TOLERANCE + BLOCK_SIZE) // BLOCK_SIZE - 1)
        pos.append((x, y))
        return pos

    def handle_movement(self):
        if self.mode == self.EASY and self.is_alive == True:
            self.moveRandom()
        elif self.mode == self.MEDIUM and self.is_alive == True:
            self.moveRandomWithoutBack()


    def remove_ghost(self):
        del self