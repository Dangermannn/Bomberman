import pygame
from pygame.locals import *

class SpriteTool:
    def __init__(self, fileName, cols, rows, pixels):
        self.sheet = pygame.image.load(fileName).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw , hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        #self.handle = list([0, 0])

    def draw(self, surface, cellIndex, x, y):
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])