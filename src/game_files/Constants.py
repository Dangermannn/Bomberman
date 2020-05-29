import pygame

# screen must be defined here just to let images load as a variable
screen = pygame.display.set_mode((750, 750))

BACKGROUND_IMG = pygame.image.load('Images/Mapv2.png')
STONE_IMG = pygame.image.load('Images/stone.png')
HEART_IMG = pygame.transform.scale((pygame.image.load('Images/heart.png').convert_alpha()), (25, 25))
MENU_BACKGROUND_IMG = pygame.image.load('Images/menuBackground.png')
BOMB_IMAGE = pygame.image.load('Images/bombv1.png')
ICON_IMG = pygame.image.load('Images/whiteGhost.png')

BOMB_SPRITE_PATH = "Images/BombSprit.png" #path cuz SpriteTool requires a direct path to the image
HERO_IMG_PATH = "Images/Hero.png"
WHITE_GHOST_PATH = 'Images/whiteGhost.png'
BLUE_GHOST_PATH = 'Images/blueGhost.png'
RED_GHOST_PATH = 'Images/redGhost.png'

TRANSPARENT_SURFACE = pygame.Surface((750, 50))
TRANSPARENT_SURFACE.set_alpha(128)

EASY = 1
MEDIUM = 2
HARD = 3

BLOCK_SIZE = 50

WALL, CLEAR, GOAL, STONE = '#', ' ', 'P', 'S'
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

GAME_MAP_STR = """\
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