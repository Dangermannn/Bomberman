import pygame


screen = pygame.display.set_mode((750, 750))
background = pygame.image.load('Images/Mapv2.png')
stone = pygame.image.load('Images/stone.png')
pygame.display.set_caption('Bomberman')
icon = pygame.image.load('Images/gosc124.png')
pygame.display.set_icon(icon)

game_map = []
BLOCK_SIZE = 50

game_map_str =  """\
###############
#   # # # #   #
# #   SSS   #S#
#   #S#S#S#SSS#
## ##S#S#S##S##
#   S         #
# # ####### # #
#             #
# ### # # ### #
#             #
## ## # # ## ##
#   # # # #   #
# #         # #
#   # # # #   #
###############
"""


def generateMap(game_map):
	for line_str in game_map_str.splitlines():
		game_map.append(list(line_str))

stoneBlocks = []
#generateMap(game_map)

def placeStones():
	for i in range(len(game_map)):
		for j in range(len(game_map[i])):
			if game_map[i][j] == 'S':
				#stoneBlocks.append((i, j))
				screen.blit(stone, (BLOCK_SIZE * i, BLOCK_SIZE * j))

def drawMap():
	for x in game_map:
		print(x)