from src.GameInitialisation import *
from src.Characters.Player import *
from src.Characters.Ghost import *
import pygame
import time
from pygame.locals import *
import tracemalloc
from src.Tools.SpriteTool import SpriteTool
from threading import Thread
# posX, posY, health, speed, bombsAmount, bombRange, imgName
EASY = 1
MEDIUM = 2

ch1 = Player(50, 80, 3, 3, 10, 5, 'Images/Hero.png')
g1 = Ghost(650, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
g2 = Ghost(50, 50, 1, 3, 2, 1, 'Images/whiteGhost.png', MEDIUM)


ghosts_list = []
ghosts_list.append(g1)
ghosts_list.append(g2)


last_time = time.time()
last_time_explosion = time.time()
pygame.init()

running = True

clock = pygame.time.Clock()

def endfunc():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

explosion_step = 0
generateMap(game_map)

while running:
    start_time = time.time()
    #screen.fill((0, 0, 0))
    screen.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    #getStones()
    placeStones()

    ch1.handleMovement()


    for g in ghosts_list:
        g.handleMovement()
    #print(isIntersection(ch1.PositionX + 10, ch1.PositionY + 10))
    if last_time != None:
        now = time.time()
        if now - last_time > 0.5:
            #print("Last time: ", last_time, " Current time: ", now)
            if ch1.isBombAddedToList():
                # ch1.BombList[0].setPosition(ch1.PositionX, ch1.PositionY)
                #ch1.setBombsOnMap()
                #ch1.BombList.explosion(now)
                last_time = now
            #Thread(target = ch1.checkExplosion(last_time_explosion, d)).start()
            ch1.checkExplosion(ghosts_list, ch1.getPlayerPositionOnMap(), )
            if now - last_time_explosion > 0.1:
                last_time_explosion = now
                explosion_step += 1
    print("HEALTH: ", ch1.Health)

    ch1.setBombsOnMap()
    end_time = (start_time - time.time()) * 1000;
    #print("PLAY POS [X, Y] = [",ch1.PositionX, ", ", ch1.PositionY, "]")
    #drawMap()
    #print("-#-#-#______________________________________#-3-3-")
    #if explosion_step == 40:
     #   game_map[2][4] = ' '
    endfunc()
    pygame.display.update()
    pygame.time.wait(int(end_time))
    #clock.tick(60)
