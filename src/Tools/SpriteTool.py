import pygame
from pygame.locals import *

class SpriteTool:
    def __init__(self, fileName, cols, rows, pixels):
        #self.sheet = pygame.image.load(fileName).convert_alpha()
        self.sheet = pygame.transform.scale((pygame.image.load(fileName).convert_alpha()), (350, 150))
        self.sheetVertical = pygame.transform.rotate(pygame.transform.scale(
            (pygame.image.load(fileName).convert_alpha()), (350, 150)), 90)
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw , hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h + 4, w, h) for index in range(self.totalCellCount)])
        self.cellsRotated = list([(int(index / cols) * h + 4, index % cols * w, w, h) for index in range(self.totalCellCount)])
        #self.handle = list([0, 0])

    def draw(self, surface, cellIndex, x, y):
        """
        Drawing cellIndex frame on position (x, y) on surface (horizontal)
        :param surface: screen
        :param cellIndex: frame index
        :param x: position x
        :param y: position y
        :return:
        """
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])
        
    def drawVertical(self, surface, cellIndex, x, y):
        """
        Drawing cellIndex frame on position (x, y) on surface (vertical)
        :param surface: screen
        :param cellIndex: frame index
        :param x: position x
        :param y: position y
        :return:
        """
        surface.blit(self.sheetVertical, (x, y), self.cellsRotated[cellIndex])