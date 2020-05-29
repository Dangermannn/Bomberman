import pygame

class Button():
    def __init__(self, color, position_x, position_y, width, height, font_size, text=''):
        self.color = color
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

    def draw(self, screen, text_colour, outline=None):
        if outline:
            temp = (self.position_x - 2, self.position_y - 2, self.width + 4, self.height + 4)
            pygame.draw.rect(screen, outline, temp, 0)
        temp = (self.position_x, self.position_y, self.width, self.height)
        pygame.draw.rect(screen, self.color, temp, 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)
            text = font.render(self.text, 1, (text_colour[0], text_colour[1], text_colour[2]))
            temp_x = self.position_x + (self.width / 2 - text.get_width() / 2)
            temp_y = (self.position_y + (self.height / 2 - text.get_height() / 2))
            screen.blit(text, (temp_x, temp_y))

    def mouse_hover(self, pos):
        """
        :param pos: mouse position
        :return: True if mouse position is on the field of button, otherwise False
        """
        if pos[0] > self.position_x and pos[0] < self.position_x + self.width:
            if pos[1] > self.position_y and pos[1] < self.position_y + self.height:
                return True
        return False
