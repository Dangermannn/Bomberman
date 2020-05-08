from src.GameInitialisation import *
from src.Characters.Player import *
from src.Characters.Ghost import *
from src.Tools.Button import *
import pygame
import time
from pygame.locals import *
from pygame import mixer
import tracemalloc
from src.Tools.SpriteTool import SpriteTool
from threading import Thread
# posX, posY, health, speed, bombsAmount, bombRange, imgName
EASY = 1
MEDIUM = 2
# player speed - 3 MIN

pygame.mixer.init()
mixer.music.load('Sounds/TheFatRat-Xenogenesis.wav')
mixer.music.set_volume(0.2)
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
    mixer.music.play(loops=-1)
    while True:
        screen.fill(pygame.Color("black"))
        screen.blit(menuBackground, (0, 0))
        startButton.draw(screen, (0, 0, 0))
        endButton.draw(screen, (255, 255, 255))
        aboutButton.draw(screen, (255, 255, 255))

        print_about_game(show_about)
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
                    mixer.music.stop()
                    mixer.music.rewind()
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
    if player.is_alive:
        return False
    loseSound = mixer.Sound("Sounds/SadTrombone-GamingSoundEffect.wav")
    loseSound.play()
    return True

def controlEndLevel():
    if not ghosts_list:
        winSound = mixer.Sound("Sounds/Victory-Sound Effect.wav")
        winSound.play()
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

        place_stones()

        # upper info bar
        screen.blit(transparent_surface, (0, 0))
        print_label("Player's lifes:", 0, 0, 20)
        for x in range(0, player.health):
            screen.blit(heart, (x * 40, 20))
        print_label("Bombs amount: " + str(player.bomb_amount), 200, 15, 30)
        print_label("Bombs' range: " + str(player.bomb_range), 400, 15, 30)
        print_label("Level: " + str(level), 600, 15, 30)
        player.handle_movement()

        for g in ghosts_list:
            g.handle_movement()
        if last_time != None:
            now = time.time()
            if now - last_time > 0.5: # 0.5
                #player.collision_with_ghosts(ghosts_list)
                if player.is_bomb_added_to_list():
                    last_time = now
        if time.time() - last_time_collision_with_ghost > 1.0:
            player.collision_with_ghosts(ghosts_list)
            last_time_collision_with_ghost = time.time()
        player.check_explosion(ghosts_list, player.get_player_position_on_map())
        player.set_bombs_on_map()
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



    generate_map(game_map)
    ghosts_list = []

    #ch1.set_to_default()
    place_stones()
    ghosts_list.clear()
    ghosts_list.append(g1)
    ghosts_list.append(g2)
    print("INIT LIST: ", ghosts_list)
    transparent_surface = pygame.Surface((750, 750))
    transparent_surface.set_alpha(128)
    transparent_surface.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    level_iterator = 1
    ch1.set_position(ch1.default_position[0], ch1.default_position[1])
    place_stones()

    for g in ghosts_list:
        g.set_position(g.default_position[0], g.default_position[1])

    screen.blit(transparent_surface, (0, 0))
    print_label("LEVEL " + str(level_iterator), 300, 300, 40)

    pygame.display.update()

    pygame.time.wait(1000)

    while running:
        if mainGame(ch1, ghosts_list, level_iterator) == False:
            level_iterator += 1

            ghosts_list.clear()
            ghosts_list.append(g1)
            ghosts_list.append(g2)

            for g in ghosts_list:
                g.set_to_default()
            ch1.set_to_default()

            if level_iterator > 5:
                if ch1.bomb_amount > 1:
                    ch1.bomb_amount -= 1
                    ch1.bomb_range -=1

            if level_iterator > 10:
                if ch1.speed >= 3:
                    ch1.speed -= 1

            if level_iterator > 15:
                if ch1.health > 1:
                    ch1.health -= 1

            game_map.clear()
            generate_map(game_map)
            place_stones()

            screen.blit(transparent_surface, (0, 0))
            print_label("LEVEL " + str(level_iterator), 300, 300, 40)

            pygame.display.update()
            pygame.time.wait(3000)

        else:
            print(ch1.is_bomb_added_to_list())
            screen.blit(transparent_surface, (0, 0))
            print_label("YOU'VE LOST", 260, 320, 60)
            pygame.display.update()
            pygame.time.wait(2000)
            break