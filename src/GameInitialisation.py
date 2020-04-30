import pygame


screen = pygame.display.set_mode((750, 750))
background = pygame.image.load('Images/Mapv2.png')
stone = pygame.image.load('Images/stone.png')
pygame.display.set_caption('Bomberman')
icon = pygame.image.load('Images/whiteGhost.png')
heart = pygame.transform.scale((pygame.image.load('Images/heart.png').convert_alpha()), (25, 25))
pygame.display.set_icon(icon)

game_map = []
BLOCK_SIZE = 50

game_map_str =  """\
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
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
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

def printLabel(text, x, y, fontSize):
	font = pygame.font.SysFont('comicsans', fontSize)
	screen.blit(render(text, font), (x, y))
	
def generateMap(game_map):
	for line_str in game_map_str.splitlines():
		print(line_str)
		game_map.append(list(line_str))

stoneBlocks = []

def placeStones():
	for i in range(len(game_map)):
		for j in range(len(game_map[i])):
			if game_map[i][j] == 'S':
				screen.blit(stone, (BLOCK_SIZE * i, BLOCK_SIZE * j))

def drawMap():
	for x in game_map:
		print(x)