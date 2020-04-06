from src.GameInitialisation import *
from src.Characters.Player import *
import pygame
import time
from pygame.locals import *
import tracemalloc
from src.Tools.SpriteTool import SpriteTool
from threading import Thread
ch1 = Player(50, 80, 3, 3, 55, 2, 'Images/gosc124.png')
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

while running:
    start_time = time.time()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    placeStones()
    s.draw(screen, (explosion_step % 7) + 7 , 50, 50)

    ch1.handleMovement()
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
            ch1.checkExplosion(explosion_step)
            if now - last_time_explosion > 0.1:
                last_time_explosion = now
                explosion_step += 1
    ch1.setBombsOnMap()
    end_time = (start_time - time.time()) * 1000;

    endfunc()
    pygame.display.update()
    pygame.time.wait(int(end_time))
    #clock.tick(60)
