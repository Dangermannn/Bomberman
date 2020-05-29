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
        main_hero = Characters.Player(50, 50, 5, 8, 13, 13, Constants.HERO_IMG_PATH)
        ghost_easy = Characters.Ghost(650, 50, 1, 4, 2, 1, Constants.WHITE_GHOST_PATH, Constants.EASY)
        ghost_medium = Characters.Ghost(50, 650, 1, 3, 2, 1, Constants.BLUE_GHOST_PATH, Constants.MEDIUM)
        ghost_hard = Characters.Ghost(650, 650, 1, 1, 1, 1, Constants.RED_GHOST_PATH, Constants.HARD)
        init.game_map.clear()
        init.generate_map(init.game_map)
        #init.place_stones()
        ghosts_list = []
        init.game_map[main_hero.last_position.x][main_hero.last_position.y] = 'P'
        init.place_stones()
        ghosts_list.clear()
        ghosts_list.append(ghost_easy)
        ghosts_list.append(ghost_medium)
        ghosts_list.append(ghost_hard)
        transparent_surface = pygame.Surface((750, 750))
        transparent_surface.set_alpha(128)
        transparent_surface.fill((0, 0, 0))
        Constants.screen.blit(Constants.BACKGROUND_IMG, (0, 0))
        level_iterator = 1
        main_hero.set_position(main_hero.default_position.x, main_hero.default_position.y)
        init.place_stones()

        for ghost in ghosts_list:
            ghost.set_position(ghost.default_position.x, ghost.default_position.y)

        Constants.screen.blit(transparent_surface, (0, 0))
        init.print_label("LEVEL " + str(level_iterator), 300, 300, 40)

        pygame.display.update()
        pygame.time.wait(1000)

        while True:
            if not main.main_game(main_hero, ghosts_list, level_iterator):
                level_iterator += 1
                ghosts_list.clear()
                ghosts_list.append(ghost_easy)
                ghosts_list.append(ghost_medium)
                ghosts_list.append(ghost_hard)
                for g in ghosts_list:
                    g.set_to_default()
                main_hero.set_to_default()
                if level_iterator > 5:
                    if main_hero.bomb_amount > 1:
                        main_hero.reduce_bomb_amout_by_one()
                        main_hero.reduce_bomb_range_by_one()
                if level_iterator > 10:
                    if main_hero.speed >= 3:
                        main_hero.reduce_speed_by_one()
                if level_iterator > 15:
                    if main_hero.health > 1:
                        main_hero.reduce_health_by_one()
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
