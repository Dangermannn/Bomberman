from src.GameInterface.MainGame import *
from src.GameInterface.Menu import *
# posX, posY, health, speed, bombsAmount, bombRange, imgName

# player speed - 3 MIN

pygame.init()

running = True

# ---------------------- MAIN LOOP ---------------------------
menu = Menu()
main = MainGame()
while True:
    menu.menu()
    ch1 = Player(50, 50, 5, 8, 13, 13, 'Images/Hero.png')
    g1 = Ghost(650, 50, 1, 4, 2, 1, 'Images/whiteGhost.png', EASY)
    g2 = Ghost(50, 650, 1, 3, 2, 1, 'Images/blueGhost.png', MEDIUM)
    g3 = Ghost(650, 650, 1, 1, 1, 1, 'Images/redGhost.png', HARD)

    game_map.clear()
    generate_map(game_map)
    place_stones()
    ghosts_list = []

    game_map[ch1.last_position[0]][ch1.last_position[1]] = 'P'
    place_stones()
    ghosts_list.clear()
    ghosts_list.append(g1)
    ghosts_list.append(g2)
    ghosts_list.append(g3)
    
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
        if main.main_game(ch1, ghosts_list, level_iterator) == False:
            level_iterator += 1

            ghosts_list.clear()
            ghosts_list.append(g1)
            ghosts_list.append(g2)
            ghosts_list.append(g3)
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
            screen.blit(transparent_surface, (0, 0))
            print_label("YOU'VE LOST", 260, 320, 60)
            pygame.display.update()
            pygame.time.wait(2000)
            break