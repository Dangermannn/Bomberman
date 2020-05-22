import pygame

class SpriteTool:
    """
    Class loading sprite image to memory and drawing on the screen in the particular area
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, file_name, cols, rows):

        temp = pygame.image.load(file_name).convert_alpha()
        self.sheet = pygame.transform.scale((temp), (350, 150))
        self.sheet_vertical = pygame.transform.rotate(pygame.transform.scale(
            (pygame.image.load(file_name).convert_alpha()), (350, 150)), 90)
        self.cols = cols
        self.rows = rows
        self.total_cell_count = cols * rows
        self.rect = self.sheet.get_rect()
        width = self.cell_width = int(self.rect.width / cols)
        height = self.cell_height = int(self.rect.height / rows)
        self.cells = list([(index%cols*width, int(index/cols)*height+4, width, height) \
                           for index in range(self.total_cell_count)])
        self.cells_rotated = list([(int(index / cols)*height+4, index%cols*width, width, height) \
                                   for index in range(self.total_cell_count)])
    def draw(self, surface, cell_index, x_coordinate, y_coordinate):
        """
        Drawing cellIndex frame on position (x_coordinate, y_coordinate) on surface (horizontal)
        :param surface: screen
        :param cell_index: frame index
        :param x_coordinate: position x_coordinate
        :param y_coordinate: position y_coordinate
        :return:
        """
        surface.blit(self.sheet, (x_coordinate, y_coordinate), self.cells[cell_index])
    def draw_vertical(self, surface, cell_index, x_coordinate, y_coordinate):
        """
        Drawing cellIndex frame on position (x_coordinate, y_coordinate) on surface (vertical)
        :param surface: screen
        :param cell_index: frame index
        :param x_coordinate: position x_coordinate
        :param y_coordinate: position y_coordinate
        :return:
        """
        temp = (x_coordinate, y_coordinate)
        surface.blit(self.sheet_vertical, temp, self.cells_rotated[cell_index])
