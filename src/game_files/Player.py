from src.game_files import Character
from src.game_files.GameInitialisation import *
from pygame import mixer
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
        gridX = (self.position_x + 20)//BLOCK_SIZE * BLOCK_SIZE + 3
        gridY = (self.position_y + 20)//BLOCK_SIZE * BLOCK_SIZE + 3
        if pressed[pygame.K_SPACE]:
            if self.bomb_amount > 0:
                popSound = mixer.Sound("Sounds/Pop-Sound Effect.wav")
                popSound.play()
                self.bomb_list.append(Bomb(gridX, gridY, self.bomb_range, time.time()))
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
                #     game_map[x][y] = ' '
                #     self.Score += 10
        self.health = hp[0]
        if self.health == 0:
            self.is_alive = False

    def get_player_position_on_map(self):
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