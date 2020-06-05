import pygame
# screen must be defined here just to let images load as a variable


class Assets:
    """
    Class storing assets
    """
    @staticmethod
    def load():
        Assets.BACKGROUND_IMG = pygame.image.load('Images/Mapv2.png')
        Assets.STONE_IMG = pygame.image.load('Images/stone.png')
        Assets.HEART_IMG = pygame.transform.scale((pygame.image.load('Images/heart.png').convert_alpha()), (25, 25))
        Assets.MENU_BACKGROUND_IMG = pygame.image.load('Images/menuBackground.png')
        Assets.BOMB_IMAGE = pygame.image.load('Images/bombv1.png')
        Assets.ICON_IMG = pygame.image.load('Images/whiteGhost.png')
        Assets.WIN_SOUND = pygame.mixer.Sound("Sounds/Victory-Sound Effect.wav")
        Assets.LOSE_SOUND = pygame.mixer.Sound("Sounds/SadTrombone-GamingSoundEffect.wav")
        Assets.EXPLOSION_SOUND = pygame.mixer.Sound('Sounds/bombExplosion.wav')

BOMB_SPRITE_PATH = "Images/BombSprit.png" #path cuz SpriteTool requires a direct path to the image
HERO_IMG_PATH = "Images/Hero.png"
WHITE_GHOST_PATH = 'Images/whiteGhost.png'
BLUE_GHOST_PATH = 'Images/blueGhost.png'
RED_GHOST_PATH = 'Images/redGhost.png'

TRANSPARENT_SURFACE = pygame.Surface((750, 50))
TRANSPARENT_SURFACE.set_alpha(128)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (51, 51, 255)
DARK_BLUE = (10, 10, 150)
RED = (255, 0, 0)
LIME = (51, 255, 51)
BURGUNDY = (150, 0, 0)
DARK_GREEN = (51, 170, 51)
BRIGHT_GREEN = (51, 255, 51)
PURPLE = (51, 51, 200)

EASY = 1
MEDIUM = 2
HARD = 3

DEFAULT_PLAYER_XY = 50
DEFAULT_PLAYER_HP = 5
DEFAULT_PLAYER_SPEED = 6
DEFAULT_PLAYER_BOMB_AMOUNT_RANGE = 13

IMG_SCALING_WIDTH_HEIGHT = 40

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
