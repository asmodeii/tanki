__author__ = 'Pawel Kalecinski'
import pygame

pygame.init()

RED = (255, 0, 0)
ORANGE = (255, 180, 0)

class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=RED, (position_x, position_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.position_x = position_x
        self.position_y = position_y
        self.position = position_x, position_y
        self.is_selected = False
        self.func = None

    def set_position(self, x_1, y_1):
        self.position = (x_1, y_1)
        self.position_x = x_1
        self.position_y = y_1

    def set_color(self, color):
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)

    def mouse_selection(self, (pos_x, pos_y)):
        if pos_x >= self.position_x and (pos_x <= self.position_x + self.width):
            if pos_y >= self.position_y and \
                    (pos_y <= self.position_y + self.height):
                return True
        return False






