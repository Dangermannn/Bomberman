import pygame
from src.game_files import Menu, MainGame, Button, Characters, SpriteTool, Constants, GameInitialisation as init

pygame.init()

running = True

# ---------------------- MAIN LOOP ---------------------------
def main_game_func():
    menu = Menu.Menu()
    main = MainGame.MainGame()
    while True:
        menu.menu()
        ch1 = Characters.Player(50, 50, 5, 8, 13, 13, Constants.HERO_IMG_PATH)
        g1 = Characters.Ghost(650, 50, 1, 4, 2, 1, Constants.WHITE_GHOST_PATH, Constants.EASY)
        g2 = Characters.Ghost(50, 650, 1, 3, 2, 1, Constants.BLUE_GHOST_PATH, Constants.MEDIUM)
        g3 = Characters.Ghost(650, 650, 1, 1, 1, 1, Constants.RED_GHOST_PATH, Constants.HARD)
        init.game_map.clear()
        init.generate_map(init.game_map)
        #init.place_stones()
        ghosts_list = []
        init.game_map[ch1.last_position[0]][ch1.last_position[1]] = 'P'
        init.place_stones()
        ghosts_list.clear()
        ghosts_list.append(g1)
        ghosts_list.append(g2)
        ghosts_list.append(g3)
        transparent_surface = pygame.Surface((750, 750))
        transparent_surface.set_alpha(128)
        transparent_surface.fill((0, 0, 0))
        Constants.screen.blit(Constants.BACKGROUND_IMG, (0, 0))
        level_iterator = 1
        ch1.set_position(ch1.default_position[0], ch1.default_position[1])
        init.place_stones()

        for g in ghosts_list:
            g.set_position(g.default_position[0], g.default_position[1])

        Constants.screen.blit(transparent_surface, (0, 0))
        init.print_label("LEVEL " + str(level_iterator), 300, 300, 40)

        pygame.display.update()

        pygame.time.wait(1000)

        while running:
            if not main.main_game(ch1, ghosts_list, level_iterator):
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
                        ch1.bomb_range -= 1
                if level_iterator > 10:
                    if ch1.speed >= 3:
                        ch1.speed -= 1
                if level_iterator > 15:
                    if ch1.health > 1:
                        ch1.health -= 1
                init.game_map.clear()
                init.generate_map(init.game_map)
                init.place_stones()
                Constants.screen.blit(transparent_surface, (0, 0))
                init.print_label("LEVEL " + str(level_iterator), 300, 300, 40)
                pygame.display.update()
                pygame.time.wait(3000)
            else:
                Constants.screen.blit(transparent_surface, (0, 0))
                init.print_label("YOU'VE LOST", 260, 320, 60)
                pygame.display.update()
                pygame.time.wait(2000)
                break

if __name__ == '__main__':
    main_game_func()
