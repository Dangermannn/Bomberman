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
# player speed - 3 MIN


pygame.init()

running = True

clock = pygame.time.Clock()


def endfunc():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()


def menu():
    startButton = Button((51, 51, 255), 70, 70, 100, 50, 21, "Start game")
    endButton = Button((255, 0, 0), 300, 70, 100, 50, 21, "Quit")
    aboutButton = Button((51, 255, 51), 500, 70, 100, 50, 21, "About game")
    show_about = False
    while True:
        screen.fill(pygame.Color("black"))
        screen.blit(menuBackground, (0, 0))
        startButton.draw(screen, (0, 0, 0))
        endButton.draw(screen, (255, 255, 255))
        aboutButton.draw(screen, (255, 255, 255))

        printAboutGame(show_about)
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
                if aboutButton.mouseHover(pos):
                    show_about = True

            if event.type == pygame.MOUSEMOTION:
                if startButton.mouseHover(pos):
                    startButton.color = (10, 10, 150)
                else:
                    startButton.color = (51, 51, 255)

                if endButton.mouseHover(pos):
                    endButton.color = (255, 0, 0)
                else:
                    endButton.color = (150, 0, 0)

                if aboutButton.mouseHover(pos):
                    aboutButton.color = (51, 170, 51)
                else:
                    aboutButton.color = (51, 255, 51)

def controlEndGame(player):
    if player.IsAlive:
        return False
    return True

def controlEndLevel():
    if not ghosts_list:
        return True
    return False

def mainGame(player, ghost_list, level):
    last_time = time.time()
    last_time_collision_with_ghost = time.time()
    transparent_surface = pygame.Surface((750, 50))
    transparent_surface.set_alpha(128)
    explosion_step = 0
    leaveButton = Button((51, 51, 255), 700, 15, 50, 30, 21, "Leave")
    while True:
        start_time = time.time()
        #screen.fill((0, 0, 0))
        screen.fill(pygame.Color("black"))
        screen.blit(background, (0, 0))

        leaveButton.draw(screen, (255, 255, 255))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if leaveButton.mouseHover(pos):
                    return True
            if event.type == pygame.MOUSEMOTION:
                if leaveButton.mouseHover(pos):
                    leaveButton.color = (10, 10, 150)
                else:
                    leaveButton.color = (51, 51, 255)

        placeStones()

        # upper info bar
        screen.blit(transparent_surface, (0, 0))
        printLabel("Player's lifes:", 0, 0, 20)
        for x in range(0, player.Health):
            screen.blit(heart, (x * 40, 20))
        printLabel("Bombs amount: " + str(player.BombsAmount), 200, 15, 30)
        printLabel("Bombs' range: " + str(player.BombRange), 400, 15, 30)
        printLabel("Level: " + str(level), 600, 15, 30)
        player.handleMovement()

        for g in ghosts_list:
            g.handleMovement()
        if last_time != None:
            now = time.time()
            if now - last_time > 0.5: # 0.5
                #player.collisionWithGhosts(ghosts_list)
                if player.isBombAddedToList():
                    last_time = now
        if time.time() - last_time_collision_with_ghost > 1.0:
            player.collisionWithGhosts(ghosts_list)
            last_time_collision_with_ghost = time.time()
        player.checkExplosion(ghosts_list, player.getPlayerPositionOnMap())
        player.setBombsOnMap()
        end_time = (start_time - time.time()) * 1000;
        endfunc()
        pygame.display.update()
        pygame.time.wait(int(end_time))
        #clock.tick(60)
        if controlEndGame(ch1):
            return True
        if controlEndLevel():
            return False




# ---------------------- MAIN LOOP ---------------------------
while True:
    menu()

    ch1 = Player(50, 50, 5, 6, 13, 13, 'Images/Hero.png')
    g1 = Ghost(650, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
    g2 = Ghost(50, 650, 1, 3, 2, 1, 'Images/blueGhost.png', MEDIUM)



    generateMap(game_map)
    ghosts_list = []

    #ch1.setToDefault()
    placeStones()
    ghosts_list.clear()
    ghosts_list.append(g1)
    ghosts_list.append(g2)
    print("INIT LIST: ", ghosts_list)
    transparent_surface = pygame.Surface((750, 750))
    transparent_surface.set_alpha(128)
    transparent_surface.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    level_iterator = 1
    ch1.setPosition(ch1.DefaultPosition[0], ch1.DefaultPosition[1])
    placeStones()

    for g in ghosts_list:
        g.setPosition(g.DefaultPosition[0], g.DefaultPosition[1])

    screen.blit(transparent_surface, (0, 0))
    printLabel("LEVEL " + str(level_iterator), 300, 300, 40)

    pygame.display.update()

    pygame.time.wait(1000)

    while running:
        if mainGame(ch1, ghosts_list, level_iterator) == False:
            level_iterator += 1

            ghosts_list.clear()
            ghosts_list.append(g1)
            ghosts_list.append(g2)

            for g in ghosts_list:
                g.setToDefault()
            ch1.setToDefault()

            if level_iterator > 5:
                if ch1.BombsAmount > 1:
                    ch1.BombsAmount -= 1
                    ch1.BombRange -=1

            if level_iterator > 10:
                if ch1.Speed >= 3:
                    ch1.Speed -= 1

            if level_iterator > 15:
                if ch1.Health > 1:
                    ch1.Health -= 1

            game_map.clear()
            generateMap(game_map)
            placeStones()

            screen.blit(transparent_surface, (0, 0))
            printLabel("LEVEL " + str(level_iterator), 300, 300, 40)

            pygame.display.update()
            pygame.time.wait(1000)

        else:
            print(ch1.isBombAddedToList())
            screen.blit(transparent_surface, (0, 0))
            printLabel("YOU'VE LOST", 260, 320, 60)
            pygame.display.update()
            pygame.time.wait(2000)
            break