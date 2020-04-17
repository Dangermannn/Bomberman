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
ch1 = Player(50, 80, 3, 3, 2, 1, 'Images/gosc124.png')
g1 = Ghost(651, 51, 3, 4, 2, 1, 'Images/whiteGhost.png')
last_time = time.time()

last_time_explosion = time.time()
pygame.init()

running = True

clock = pygame.time.Clock()
s = SpriteTool("Images/BombSprit.png", 7, 3, 48)

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
    s.draw(screen, (explosion_step % 7) + 7 , 50, 50)

    ch1.handleMovement()
    g1.MoveRandom()
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
            ch1.checkExplosion()
            if now - last_time_explosion > 0.1:
                last_time_explosion = now
                explosion_step += 1


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
