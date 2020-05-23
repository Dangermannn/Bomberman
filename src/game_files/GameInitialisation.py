import pygame, queue, collections
import queue
import collections
from pygame import mixer

screen = pygame.display.set_mode((750, 750))
BACKGROUND_IMG = pygame.image.load('Images/Mapv2.png')
STONE_IMG = pygame.image.load('Images/stone.png')
HEART_IMG = pygame.transform.scale((pygame.image.load('Images/heart.png').convert_alpha()), (25, 25))
MENU_BACKGROUND_IMG = pygame.image.load('Images/menuBackground.png')
BOMB_IMAGE = pygame.image.load('Images/bombv1.png')
ICON_IMG = pygame.image.load('Images/whiteGhost.png')

pygame.display.set_icon(ICON_IMG)
pygame.display.set_caption('Bomberman')
pygame.mixer.init()
mixer.music.load('Sounds/TheFatRat-Xenogenesis.wav')
mixer.music.set_volume(0.2)

TRANSPARENT_SURFACE = pygame.Surface((750, 50))
TRANSPARENT_SURFACE.set_alpha(128)

EASY = 1
MEDIUM = 2
HARD = 3

BLOCK_SIZE = 50

WALL, CLEAR, GOAL, STONE = '#', ' ', 'P', 'S',
WIDTH, HEIGHT = 15, 15

ABOUT_MESSAGE_STR = """\
Your main goal is to kill all the ghosts walking around the map.
        The thing is you cannot allow them catch you!

        By going to next levels your statistics will get worse.
                
                            LEVEL > 5
         Bombs amount and bomb range as well are decreasing
                    
                             LEVEL > 10
                     Speed is being decreased
                             
                            LEVEL > 15
          Your health is decreasing (cannot die because of it)
                             
                         KEY UP - move up
                        KEY DOWN - move down
                        KEY LEFT - move left
                        KEY RIGHT - move right
                        SPACEBAR - place a bomb


                        GOOD LUCK!
"""

GAME_MAP_STR =  """\
###############
#   # # # #   #
# #   SSS   # #
#  S#S# #S#S S#
## ##S# #S##S##
#   S  S S  S #
#S#S#######S#S#
#   S  S S    #
# ### # # ### #
# S S S S S S #
## ## # # ## ##
#   #S# #S# S #
# #S  SSS S # #
#   # # # #   #
###############
"""

about_message = []

show_about = False

game_map = []

stoneBlocks = []


for line_str in ABOUT_MESSAGE_STR.splitlines():
    about_message.append(line_str)

# functions to add outline to the text

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points.extend([(y, x) for x, y in points if x > y])
    points.extend([(-x, y) for x, y in points if x])
    points.extend([(x, -y) for x, y in points if y])
    #points += [(y, x) for x, y in points if x > y]
    #points += [(-x, y) for x, y in points if x]
    #points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(0, 0, 0), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

def print_label(text, x, y, fontSize):
	font = pygame.font.SysFont('comicsans', fontSize)
	screen.blit(render(text, font), (x, y))
	
def generate_map(game_map):
	for line_str in GAME_MAP_STR.splitlines():
		game_map.append(list(line_str))

def place_stones():
	for i in range(len(game_map)):
		for j in range(len(game_map[i])):
			if game_map[i][j] == 'S':
				screen.blit(STONE_IMG, (BLOCK_SIZE * i, BLOCK_SIZE * j))

def show_stats(player, level, x, y):
    font_s = pygame.font.SysFont("comicsans", 32)
    score = font_s.render("Bombs amount/range: " + str(player.bomb_amount) + " Level: " + str(level), True, (255, 255, 255))
    screen.blit(score, (x, y))

def print_about_game(boolean):
    if boolean == True:
        add = 0
        for x in about_message:
            print_label(x, 150, 230 + add, 21)
            add += 20

def mark_player_on_map(player):
    if player.last_position != player.get_player_position_on_map():
        game_map[player.last_position[0]][player.last_position[1]] = ' '
        player.last_position = player.get_player_position_on_map()
        game_map[player.last_position[0]][player.last_position[1]] = 'P'

# PATH FINDING ALGORITHM

def find_shortest_path(grid, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[x][y] == GOAL:
            return path
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= x2 < WIDTH and 0 <= y2 < HEIGHT and grid[x2][y2] != WALL and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
