import random, collections, pygame, os, time
from pygame import mixer, Surface
from src.game_files import Bomb, Constants, GameInitialisation as init

X_SPEED_CHANGE = {
    pygame.K_LEFT: -1,
    pygame.K_RIGHT: +1,
}

Y_SPEED_CHANGE = {
    pygame.K_UP: -1,
    pygame.K_DOWN: +1,
}

class Character:
    FREE_WAY = [' ', 'P']

    def __init__(self, position_x = 50, position_y = 50, health = 5, speed = 6,
                 bomb_amount = 13, bomb_range = 13, image_name=Constants.HERO_IMG_PATH):
        self.position_x = position_x
        self.position_y = position_y
        self.health = health
        self.speed = speed
        self.bomb_amount = bomb_amount
        self.bomb_range = bomb_range
        self.position_x_change = 0
        self.position_y_change = 0
        self.bomb_list = []
        self.character_image = pygame.transform.scale((pygame.image.load(image_name).convert_alpha()), (40, 40))
        self.is_alive = True
        self.default_position = (position_x, position_x)
        self.last_position = (1, 1)

    def set_to_default(self):
        """
        Setting character stats to default
        """
        self.position_x = 50
        self.position_y = 50
        self.position_x_change = 0
        self.position_y_change = 0
        self.bomb_list = []
        #self.Score = 0
        self.is_alive = True

    def collision_x(self, corner):
        """
        Function for checking collision on x-coordinate. If there's no collision, player moves.
        :param corner: player's corner position
        """
        corner += self.position_x_change + Constants.BLOCK_SIZE
        lower_corner = self.position_y + self.character_image.get_height() + Constants.BLOCK_SIZE
        upper_corner = self.position_y + Constants.BLOCK_SIZE
        if (init.game_map[corner // Constants.BLOCK_SIZE - 1][upper_corner // Constants.BLOCK_SIZE - 1] in self.FREE_WAY and
            init.game_map[corner // Constants.BLOCK_SIZE - 1][lower_corner // Constants.BLOCK_SIZE - 1] in self.FREE_WAY):
            self.position_x += self.position_x_change
            return False
        return True

    def collision_y(self, corner):
        """
        Function for checking collision on x-coordinate. If there's no collision, player moves.
        :param corner: player's corner position
        """
        corner += self.position_y_change + Constants.BLOCK_SIZE
        left_corner = self.position_x + Constants.BLOCK_SIZE
        right_corner = self.position_x + self.character_image.get_width() + Constants.BLOCK_SIZE
        if (init.game_map[left_corner // Constants.BLOCK_SIZE - 1][corner // Constants.BLOCK_SIZE - 1] in self.FREE_WAY and
            init.game_map[right_corner // Constants.BLOCK_SIZE - 1][corner // Constants.BLOCK_SIZE - 1] in self.FREE_WAY):
            self.position_y += self.position_y_change
            return False
        return True
    def set_position(self, position_x, position_y):
        """
        Placing bot on map
        :param position_x: character's position
        :param position_y: character's position
        """
        Constants.screen.blit(self.character_image, (position_x, position_y))
    def reduce_health_by_one(self):
        self.health -= 1
    def set_not_alive(self):
        self.is_alive = False

class Player(Character):
    PIXEL_TOLERANCE = 5
    def handle_movement(self):
        pressed = pygame.key.get_pressed()
        for key, direction in X_SPEED_CHANGE.items():
            if pressed[key]:
                self.position_x_change = direction * self.speed
                if self.position_x_change < 0:
                    self.collision_x(self.position_x)
                else:
                    self.collision_x(self.position_x + self.character_image.get_width())
                self.position_y_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed[key]:
                self.position_y_change = direction * self.speed
                if self.position_y_change < 0:
                    self.collision_y(self.position_y)
                else:
                    self.collision_y(self.position_y + self.character_image.get_height())
                self.position_y_change = 0
        self.set_position(self.position_x, self.position_y)

    def is_bomb_added_to_list(self):
        pressed = pygame.key.get_pressed()
        gridX = (self.position_x + 20) // Constants.BLOCK_SIZE * Constants.BLOCK_SIZE + 3
        gridY = (self.position_y + 20) // Constants.BLOCK_SIZE * Constants.BLOCK_SIZE + 3
        if pressed[pygame.K_SPACE]:
            if self.bomb_amount > 0:
                popSound = mixer.Sound("Sounds/Pop-Sound Effect.wav")
                popSound.play()
                self.bomb_list.append(Bomb.Bomb(gridX, gridY, self.bomb_range, time.time()))
                self.bomb_amount -= 1
                return True
        return False

    def set_bombs_on_map(self):
        if not self.bomb_list:
            return
        for item in self.bomb_list:
            if item.show_bomb == True:
                item.set_position(item.position_x, item.position_y)

    def check_explosion(self, ghosts, playerCords):
        blocksToRemove = []
        hp = [self.health]
        isAlive = self.is_alive
        for item in self.bomb_list:
            if item.explosion(ghosts, self.get_border_positions_on_map(), hp, isAlive) == True:
                self.bomb_list.remove(item)
                self.bomb_amount += 1
                # for x, y in blocksToRemove:
                #     init.game_map[x][y] = CLEAR
                #     self.Score += 10
        #elf.health = hp[0]
        if self.health == 0:
            self.is_alive = False

    def get_player_position_on_map(self):
        x = ((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        return (x, y)

    def get_border_positions_on_map(self):
        pos = []
        x = ((self.position_x + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        pos.append((x, y))

        x = ((self.position_x + self.character_image.get_width() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.character_image.get_height() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        pos.append((x, y))
        return pos

    def collision_with_ghosts(self, ghosts):
        playerPos = []
        ghostPos = []
        playerPos = self.get_border_positions_on_map()
        for x in ghosts:
            ghostPos = x.get_border_positions_on_map()
            for p in playerPos:
                if p in ghostPos:
                    self.health -= 1
                    if self.health == 0:
                        self.is_alive = False

class Ghost(Character):
    EASY = 1
    MEDIUM = 2
    HARD = 3
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
        self.last_positions.append((((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1),
                                      ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)))
        self.is_alive = True
        self.mode = mode
        self.default_position = (position_x, position_y)

    def set_to_default(self):
        self.position_x = self.default_position[0]
        self.position_y = self.default_position[1]
        self.health = 1
        self.is_alive = True
        self.distance_traveled = 0

    def collision_x(self, corner):
        """
        Function to check ghost's collision and move him if there's not collision.
        Function is set just for bots: one move - 50 PX
        :param corner:
        :return: True if there's collision
        """
        corner += self.position_x_change + Constants.BLOCK_SIZE
        lower_corner = self.position_y + self.character_image.get_height() + Constants.BLOCK_SIZE
        upper_corner = self.position_y + Constants.BLOCK_SIZE
        if (init.game_map[corner // Constants.BLOCK_SIZE - 1][upper_corner // Constants.BLOCK_SIZE - 1] != Constants.WALL and
            init.game_map[corner // Constants.BLOCK_SIZE - 1][lower_corner // Constants.BLOCK_SIZE - 1] != Constants.WALL):
            if self.distance_traveled < self.MAX_MOVEMENT:
                self.position_x += self.position_x_change
            else:
                self.position_x += (self.MAX_MOVEMENT - self.distance_traveled)
                #self.distance_traveled = 0
            return False
        return True

    def collision_y(self, corner):
        """
        Function to check ghost's collision and move him if there's not collision.
        Function is set just for bots: one move - 50 PX
        :param corner:
        :return: True if there's collision
        """
        corner += self.position_y_change + Constants.BLOCK_SIZE
        left_corner = self.position_x + Constants.BLOCK_SIZE
        right_corner = self.position_x + self.character_image.get_width() + Constants.BLOCK_SIZE
        if (init.game_map[left_corner // Constants.BLOCK_SIZE - 1][corner // Constants.BLOCK_SIZE - 1] != Constants.WALL and
            init.game_map[right_corner // Constants.BLOCK_SIZE - 1][corner // Constants.BLOCK_SIZE - 1] != Constants.WALL):
            if self.distance_traveled < self.MAX_MOVEMENT:
                self.position_y += self.position_y_change
            else:
                self.position_y += (self.MAX_MOVEMENT - self.distance_traveled)
                #self.distance_traveled = 0
            return False
        return True

    def move_random(self):
        """
        Handling ghosts moving random
        """
        direction = random.choice(self.POSSIBLE_MOVEMENTS)
        if self.distance_traveled == 0:
            self.current_direction = direction
        pressed = self.current_direction

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

    def following_player(self):
        """
        Ghost trying to follow the player
        """
        #path_queue = collections.deque()
        try:
            if not self.possible_movements:
                path_queue = init.find_shortest_path(init.game_map, self.get_position_on_map())
                #print("Q: ", path_queue)
                if path_queue != None:
                    path_queue.reverse()
                    next_cords = path_queue.pop()
                    if next_cords == self.get_position_on_map():
                        next_cords = path_queue.pop()
                    ghost_cords = self.get_position_on_map()
                    if next_cords[0] < ghost_cords[0]:
                        self.possible_movements.append(self.POSSIBLE_MOVEMENTS[0])
                    elif next_cords[0] > ghost_cords[0]:
                        self.possible_movements.append(self.POSSIBLE_MOVEMENTS[1])

                    if next_cords[1] < ghost_cords[1]:
                        self.possible_movements.append(self.POSSIBLE_MOVEMENTS[2])
                    elif next_cords[1] > ghost_cords[1]:
                        self.possible_movements.append(self.POSSIBLE_MOVEMENTS[3])

            pressed = self.possible_movements[0]
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
                del self.possible_movements[0]
        except IndexError:
            print("out of index")
        except:
            print("Unknow error in following ghost")
        finally:
            self.set_position(self.position_x, self.position_y)

#Ghost picks random path, but cannot choose last block he was on
    def move_random_without_back(self):
        """
        Handling random moving bot. Little clever than move_random
        """
        x = ((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1) * Constants.BLOCK_SIZE
        y = ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1) * Constants.BLOCK_SIZE
        if self.distance_traveled == 0:
            x = ((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1) * Constants.BLOCK_SIZE
            y = ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1) * Constants.BLOCK_SIZE
            # available paths
            left = x
            right = x + 2 * Constants.BLOCK_SIZE
            down = y + Constants.BLOCK_SIZE
            up = y - Constants.BLOCK_SIZE
            leftSide = False
            rightSide = False
            upperSide = False
            downSide = False
            #print("-------------------------------------------------------------------")
            #print("DISTANCE TRAVELED", self.distance_traveled)
            #print("WARUNKI")
            #print("POSITION: [", x // constants.BLOCK_SIZE, ", ", y // constants.BLOCK_SIZE, "]")
            #print("LEFT: [", left // constants.BLOCK_SIZE - 1, ", ", y // constants.BLOCK_SIZE, "]", "GAME MAP: ", init.game_map[left // constants.BLOCK_SIZE - 1][y // constants.BLOCK_SIZE] )
            if (init.game_map[left // Constants.BLOCK_SIZE - 1][y // Constants.BLOCK_SIZE] != Constants.WALL):
                leftSide = True
            if (init.game_map[right // Constants.BLOCK_SIZE - 1][y // Constants.BLOCK_SIZE] != Constants.WALL):
                rightSide = True
            if (init.game_map[x // Constants.BLOCK_SIZE][up // Constants.BLOCK_SIZE] != Constants.WALL):
                upperSide = True
            if (init.game_map[x // Constants.BLOCK_SIZE][down // Constants.BLOCK_SIZE] != Constants.WALL):
                downSide = True


            #print("LAST POSITIONS: ", self.last_positions)
           # print("LEWO: ", leftSide, " PRAWO: ", rightSide, " GORA", upperSide, " DOL", downSide)
            #print("UPPER: ", (x // constants.BLOCK_SIZE, y // constants.BLOCK_SIZE - 1))
            #print("LEFT: ", (x // constants.BLOCK_SIZE - 1, y // constants.BLOCK_SIZE))
            #print("RIGHT: ", (x // constants.BLOCK_SIZE + 1, y // constants.BLOCK_SIZE))
            #print("DOWN: ", (x // constants.BLOCK_SIZE, y // constants.BLOCK_SIZE + 1))
            if (upperSide and (x // Constants.BLOCK_SIZE, y // Constants.BLOCK_SIZE - 1) not in self.last_positions) or (y // Constants.BLOCK_SIZE - 1 == 12):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[2])
               # print("APPENDED x, y : [",x // constants.BLOCK_SIZE, ", ", y // constants.BLOCK_SIZE - 1, "]")
                #print("DODAJTE GORA")
            if (leftSide and (x // Constants.BLOCK_SIZE - 1, y // Constants.BLOCK_SIZE) not in self.last_positions) or (x // Constants.BLOCK_SIZE - 1 == 12):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[0])
               # print("APPENDED x, y : [",x // constants.BLOCK_SIZE - 1, ", ", y // constants.BLOCK_SIZE, "]")
                #print("DODAJE LEWO")
            if (rightSide and (x // Constants.BLOCK_SIZE + 1, y // Constants.BLOCK_SIZE) not in self.last_positions) or (x // Constants.BLOCK_SIZE + 1 == 2):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[1])
                #print("DODAJE PRAWO")
            if (downSide and (x // Constants.BLOCK_SIZE, y // Constants.BLOCK_SIZE + 1) not in self.last_positions) or (y // Constants.BLOCK_SIZE + 1 == 2):
                self.possible_movements.append(self.POSSIBLE_MOVEMENTS[3])
               # print("DODAJE DOL")
       # print("DISTANCE: ", self.distance_traveled)
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
                        self.last_positions.append((x // Constants.BLOCK_SIZE, y // Constants.BLOCK_SIZE))
                        #print("LEFT ADDED: [", x//constants.BLOCK_SIZE, ", ", y//constants.BLOCK_SIZE, "]")
                else:
                    self.collision_x(self.position_x + self.character_image.get_width())
                    if self.distance_traveled == 0:
                        self.last_positions.append((x // Constants.BLOCK_SIZE, y // Constants.BLOCK_SIZE))
                        #print("RIGHT ADDED: [", x // constants.BLOCK_SIZE, ", ", y // constants.BLOCK_SIZE, "]")
                self.position_y_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed == key:
                self.position_y_change = direction * self.speed
                if self.position_y_change < 0:
                    self.collision_y(self.position_y)
                    if self.distance_traveled == 0:
                        self.last_positions.append((x // Constants.BLOCK_SIZE, y // Constants.BLOCK_SIZE))
                        #print("UP ADDED: [", x // constants.BLOCK_SIZE, ", ", y // constants.BLOCK_SIZE, "]")
                else:
                    self.collision_y(self.position_y + self.character_image.get_height())
                    if self.distance_traveled == 0:
                        self.last_positions.append((x // Constants.BLOCK_SIZE, y // Constants.BLOCK_SIZE))
                        #print("LEFT ADDED: [", x // constants.BLOCK_SIZE, ", ", y // constants.BLOCK_SIZE, "]")
                self.position_y_change = 0
        self.distance_traveled += self.speed
        #print("DISTANCE AFTER ADDING", self.distanceTraveled)
        if self.distance_traveled >= self.MAX_MOVEMENT:
            self.distance_traveled = 0
        self.set_position(self.position_x, self.position_y)

        self.possible_movements.clear()

    def get_position_on_map(self):
        """
        Gets ghost's position on the map
        :return: ghost's coordinates on map
        """
        x = ((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        return (x, y)


    def get_border_positions_on_map(self):
        """
        Gets ghost's borders position on the map
        :return: ghost's coordinates of borders on the amp
        """
        pos = []
        x = ((self.position_x + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        pos.append((x, y))

        x = ((self.position_x + self.character_image.get_width() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.character_image.get_height() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        pos.append((x, y))
        return pos

    def handle_movement(self):
        """
        Handling movement of ghost. It's for using one function for every created bot not depending on difficulty
        """
        if self.mode == self.EASY and self.is_alive:
            self.move_random()
        elif self.mode == self.MEDIUM and self.is_alive:
            self.move_random_without_back()
        elif self.mode == self.HARD and self.is_alive:
            self.following_player()
