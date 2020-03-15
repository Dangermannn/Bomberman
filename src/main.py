from src.GameInitialisation import *
from src.Characters.Player import *
import pygame
import time
from pygame.locals import *
import tracemalloc

ch1 = Player(50, 80, 3, 3, 4, 2, 'Images/gosc124.png')
last_time = time.time()
pygame.init()

running = True

clock = pygame.time.Clock()

def endfunc():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    ch1.handleMovement()
    if last_time != None:
        now = time.time()
        if now - last_time > 0.5:
            #print("Last time: ", last_time, " Current time: ", now)
            if ch1.isBombAddedToList():
                #ch1.BombList[0].setPosition(ch1.PositionX, ch1.PositionY)
                ch1.setBombsOnMap()
                last_time = now
    ch1.setBombsOnMap()

    endfunc()
    pygame.display.update()
    clock.tick(60)
