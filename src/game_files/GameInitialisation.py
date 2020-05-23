import pygame, queue, collections
from pygame import mixer
from src.game_files import Constants


pygame.display.set_icon(Constants.ICON_IMG)
pygame.display.set_caption('Bomberman')
pygame.mixer.init()
mixer.music.load('Sounds/TheFatRat-Xenogenesis.wav')
mixer.music.set_volume(0.2)

about_message = []

game_map = []

stoneBlocks = []


for line_str in Constants.ABOUT_MESSAGE_STR.splitlines():
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
	Constants.screen.blit(render(text, font), (x, y))
	
def generate_map(game_map):
	for line_str in Constants.GAME_MAP_STR.splitlines():
		game_map.append(list(line_str))

def place_stones():
	for i in range(len(game_map)):
		for j in range(len(game_map[i])):
			if game_map[i][j] == 'S':
				Constants.screen.blit(Constants.STONE_IMG, (Constants.BLOCK_SIZE * i, Constants.BLOCK_SIZE * j))

def show_stats(player, level, x, y):
    font_s = pygame.font.SysFont("comicsans", 32)
    score = font_s.render("Bombs amount/range: " + str(player.bomb_amount) + " Level: " + str(level), True, (255, 255, 255))
    Constants.screen.blit(score, (x, y))

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
        if grid[x][y] == Constants.GOAL:
            return path
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= x2 < Constants.WIDTH and 0 <= y2 < Constants.HEIGHT and grid[x2][y2] != Constants.WALL and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
