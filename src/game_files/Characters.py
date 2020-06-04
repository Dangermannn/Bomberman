import random
import time
import math
import pygame
from src.game_files import Bomb
from src.game_files import Constants
from src.game_files import GameInitialisation as init

X_SPEED_CHANGE = {
    pygame.K_LEFT: -1,
    pygame.K_RIGHT: +1,
}

Y_SPEED_CHANGE = {
    pygame.K_UP: -1,
    pygame.K_DOWN: +1,
}

class Character:
    """
    Base class
    """
    FREE_WAY = [' ', 'P']

    def __init__(self, position_x=Constants.DEFAULT_PLAYER_XY, position_y=Constants.DEFAULT_PLAYER_XY,
                 health=Constants.DEFAULT_PLAYER_HP, speed=Constants.DEFAULT_PLAYER_SPEED,
                 bomb_amount=Constants.DEFAULT_PLAYER_BOMB_AMOUNT_RANGE,
                 bomb_range=Constants.DEFAULT_PLAYER_BOMB_AMOUNT_RANGE,
                 image_name=Constants.HERO_IMG_PATH):
        self.position_x = position_x
        self.position_y = position_y
        self.health = health
        self.speed = speed
        self.bomb_amount = bomb_amount
        self.bomb_range = bomb_range
        self.position_x_change = 0
        self.position_y_change = 0
        self.bomb_list = []
        self.character_image = pygame.transform.scale(
            (pygame.image.load(image_name).convert_alpha()),
            (Constants.IMG_SCALING_WIDTH_HEIGHT, Constants.IMG_SCALING_WIDTH_HEIGHT))
        self.is_alive = True
        self.default_position = init.Point(position_x, position_x)
        self.last_position = init.Point(1, 1)

    def set_to_default(self):
        """
        Setting character stats to default
        """
        self.position_x = Constants.DEFAULT_PLAYER_XY
        self.position_y = Constants.DEFAULT_PLAYER_XY
        self.position_x_change = 0
        self.position_y_change = 0
        self.bomb_list = []
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

    def reduce_bomb_amout_by_one(self):
        self.bomb_amount -= 1

    def reduce_bomb_range_by_one(self):
        self.bomb_range -= 1

    def reduce_speed_by_one(self):
        self.speed -= 1

class Player(Character):
    """
    Main hero class
    """
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
        grid_x = (self.position_x + 20) // Constants.BLOCK_SIZE * Constants.BLOCK_SIZE + 3
        grid_y = (self.position_y + 20) // Constants.BLOCK_SIZE * Constants.BLOCK_SIZE + 3
        if pressed[pygame.K_SPACE]:
            if self.bomb_amount > 0:
                pop_sound = pygame.mixer.Sound("Sounds/Pop-Sound Effect.wav")
                pop_sound.play()
                self.bomb_list.append(Bomb.Bomb(grid_x, grid_y, self.bomb_range, time.time()))
                self.bomb_amount -= 1
                return True
        return False

    def set_bombs_on_map(self):
        if not self.bomb_list:
            return
        for item in self.bomb_list:
            if item.show_bomb:
                item.set_position(item.position_x, item.position_y)

    def check_explosion(self, ghosts):
        for item in self.bomb_list:
            if item.explosion(ghosts, self.get_border_positions_on_map(), self.reduce_health_by_one):
                self.bomb_list.remove(item)
                self.bomb_amount += 1
        if self.health == 0:
            self.set_not_alive()

    def get_player_position_on_map(self):
        x = ((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        return (x, y)

    def get_border_positions_on_map(self):
        pos = []
        x = ((self.position_x + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        pos.append((x, y))

        x = ((self.position_x + self.character_image.get_width() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE)
             // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.character_image.get_height() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE)
             // Constants.BLOCK_SIZE - 1)
        pos.append((x, y))
        return pos

    def collision_with_ghosts(self, ghosts):
        for ghost in ghosts:
            for position in self.get_border_positions_on_map():
                if position in ghost.get_border_positions_on_map():
                    self.health -= 1
                    if self.health == 0:
                        self.is_alive = False

class Ghost(Character):
    """
    Enemy ghost class
    """
    MAX_MOVEMENT = 50
    PIXEL_TOLERANCE = 3
    X_LEFT_BLOCK_SECURE = 1
    X_RIGHT_BLOCK_SECURE = 13
    POSSIBLE_MOVEMENTS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

    def __init__(self, position_x, position_y, health, speed, bomb_amount, bomb_range, image_name, mode):
        super(Ghost, self).__init__(position_x, position_y, health,
                                    speed, bomb_amount, bomb_range, image_name)
        self.character_image = pygame.transform.scale((pygame.image.load(image_name).convert_alpha()), (44, 44))
        self.distance_traveled = 0
        self.current_direction = None
        self.possible_movements = []
        self.last_positions = []
        self.last_positions.append(init.Point(((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1),
                                              ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)))
        self.is_alive = True
        self.mode = mode
        self.default_position = init.Point(position_x, position_y)
        self.last_move = None

    def set_to_default(self):
        self.position_x = self.default_position.x
        self.position_y = self.default_position.x
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

    def correct_position(self):
        if self.distance_traveled >= self.MAX_MOVEMENT:
            self.distance_traveled = 0
            if self.position_x % Constants.BLOCK_SIZE > Constants.BLOCK_SIZE - self.PIXEL_TOLERANCE:
                self.position_x = math.ceil(self.position_x / Constants.BLOCK_SIZE) * Constants.BLOCK_SIZE
            elif self.position_x % Constants.BLOCK_SIZE < self.PIXEL_TOLERANCE:
                self.position_x = math.floor(self.position_x / Constants.BLOCK_SIZE) * Constants.BLOCK_SIZE

            if self.position_y % Constants.BLOCK_SIZE < self.PIXEL_TOLERANCE:
                self.position_y = math.floor(self.position_y / Constants.BLOCK_SIZE) * Constants.BLOCK_SIZE
            elif self.position_y % Constants.BLOCK_SIZE > Constants.BLOCK_SIZE - self.PIXEL_TOLERANCE:
                self.position_y = math.ceil(self.position_y / Constants.BLOCK_SIZE) * Constants.BLOCK_SIZE

    def set_possible_movements_for_following_ghost(self, path_queue):
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
        try:
            if not self.possible_movements:
                path_queue = init.find_shortest_path(init.game_map, self.get_position_on_map())
                if path_queue is not None:
                    self.set_possible_movements_for_following_ghost(path_queue)

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
            pass
        except:
            print("Unknow error in following ghost")
        finally:
            self.set_position(self.position_x, self.position_y)

#Ghost picks random path, but cannot choose last block he was on
    def move_random_without_back(self):
        """
        Handling random moving bot. Little clever than move_random
        """
        if self.distance_traveled == 0:
            x = ((self.position_x + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1) * Constants.BLOCK_SIZE
            y = ((self.position_y + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1) * Constants.BLOCK_SIZE

            left_side = False
            right_side = False
            upper_side = False
            down_side = False

            current_x = x // Constants.BLOCK_SIZE
            current_y = y // Constants.BLOCK_SIZE

            if init.game_map[current_x - 1][current_y] != Constants.WALL:
                left_side = True
            if init.game_map[current_x + 1][current_y] != Constants.WALL:
                right_side = True
            if init.game_map[current_x][current_y - 1] != Constants.WALL:
                upper_side = True
            if init.game_map[current_x][current_y + 1] != Constants.WALL:
                down_side = True

            if (upper_side and (current_x, current_y - 1) not in self.last_positions):
                self.possible_movements.append(pygame.K_UP)
            if (left_side and (current_x - 1, current_y) not in self.last_positions):
                self.possible_movements.append(pygame.K_LEFT)
            if (right_side and (current_x + 1, current_y) not in self.last_positions):
                self.possible_movements.append(pygame.K_RIGHT)
            if (down_side and (current_x, current_y + 1) not in self.last_positions):
                self.possible_movements.append(pygame.K_DOWN)

            if not self.possible_movements:
                if current_x == self.X_LEFT_BLOCK_SECURE:
                    self.possible_movements.append(pygame.K_RIGHT)
                elif current_x == self.X_RIGHT_BLOCK_SECURE:
                    self.possible_movements.append(pygame.K_LEFT)

        if not self.possible_movements:
            self.possible_movements.append(None)

        if len(self.last_positions) == 6:
            self.last_positions.pop(0)

        if self.distance_traveled == 0:
            direction = random.choice(self.possible_movements)

        if self.distance_traveled == 0:
            self.current_direction = direction
        pressed = self.current_direction

        for key, direction in X_SPEED_CHANGE.items():
            if pressed == key:
                self.position_x_change = direction * self.speed
                if self.position_x_change < 0:
                    self.collision_x(self.position_x)
                    if self.distance_traveled == 0:
                        self.last_positions.append((current_x, current_y))
                else:
                    self.collision_x(self.position_x + self.character_image.get_width())
                    if self.distance_traveled == 0:
                        self.last_positions.append((current_x, current_y))
                self.position_y_change = 0

        for key, direction in Y_SPEED_CHANGE.items():
            if pressed == key:
                self.position_y_change = direction * self.speed
                if self.position_y_change < 0:
                    self.collision_y(self.position_y)
                    if self.distance_traveled == 0:
                        self.last_positions.append((current_x, current_y))
                else:
                    self.collision_y(self.position_y + self.character_image.get_height())
                    if self.distance_traveled == 0:
                        self.last_positions.append((current_x, current_y))
                self.position_y_change = 0
        self.distance_traveled += self.speed
        self.correct_position()

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
        :return: ghost's coordinates of borders on the map
        """
        pos = []
        x = ((self.position_x + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) // Constants.BLOCK_SIZE - 1)
        pos.append((x, y))

        x = ((self.position_x + self.character_image.get_width() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) //
             Constants.BLOCK_SIZE - 1)
        y = ((self.position_y + self.character_image.get_height() - self.PIXEL_TOLERANCE + Constants.BLOCK_SIZE) //
             Constants.BLOCK_SIZE - 1)
        pos.append((x, y))
        return pos

    def handle_movement(self):
        """
        Handling movement of ghost. It's for using one function for every created bot not depending on difficulty
        """
        if self.mode == Constants.EASY and self.is_alive:
            self.move_random()
        elif self.mode == Constants.MEDIUM and self.is_alive:
            self.move_random_without_back()
        elif self.mode == Constants.HARD and self.is_alive:
            self.following_player()
