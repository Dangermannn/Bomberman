import pygame


screen = pygame.display.set_mode((750, 750))
background = pygame.image.load('Images/Mapv2.png')

pygame.display.set_caption('Bomberman')
icon = pygame.image.load('Images/gosc124.png')
pygame.display.set_icon(icon)

game_map_str =  """\
###############
#   # # # #   #
# #         # #
#   # # # #   #
## ## # # ## ##
#             #
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

game_map = []

for line_str in game_map_str.splitlines():
	game_map.append(list(line_str))
	


