from src.GameInitialisation import *
from src.Characters.Player import *
from src.Characters.Ghost import *
from src.Tools.Button import *
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
explosion_step = 0
generateMap(game_map)


def endfunc():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()


def menu():
    startButton = Button((51, 51, 255), 70, 70, 100, 50, 21, "Start game")
    endButton = Button((255, 0, 0), 300, 70, 100, 50, 21, "Quit")

    while True:
        screen.fill(pygame.Color("black"))
        startButton.draw(screen, (0, 0,0))
        endButton.draw(screen, (255, 255, 255))
        pygame.display.update()
        #startButton.blitBut()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.mouseHover(pos):
                    return
                if endButton.mouseHover(pos):
                    running = False
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if startButton.mouseHover(pos):
                    print("HOVERRRRR")
                    startButton.color = (10, 10, 150)
                else:
                    startButton.color = (51, 51, 255)

                if endButton.mouseHover(pos):
                    print("HOVERRRRR")
                    endButton.color = (255, 0, 0)
                else:
                    endButton.color = (150, 0, 0)

menu()
screen.fill(pygame.Color("black"))
screen.blit(background, (0, 0))
# getStones()
ch1.handleMovement()
placeStones()
for g in ghosts_list:
    g.handleMovement()
pygame.display.update()

pygame.time.wait(1000)

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
    #print("HEALTH: ", ch1.Health)

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
