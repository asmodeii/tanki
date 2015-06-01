"""Menu Items"""
__author__ = 'Pawel Kalecinski'
import pygame

pygame.init()

RED = (255, 0, 0)
ORANGE = (255, 180, 0)

class MenuItem(pygame.font.Font):
    """Creating Menu Items"""
    def __init__(self, text, font=None, font_size=30, font_color=RED, position=(0, 0)):
        super(MenuItem, self).__init__(font, font_size)
        self.font_color = font_color
        self.text = text
        self.base_font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.position = position
        self.is_selected = False
        self.func = None

    def set_position(self, x_1, y_1):
        """set position"""
        self.position = (x_1, y_1)

    def set_color(self, color):
        """set color of font"""
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)

    def mouse_selection(self, pos):
        """ checking whether position of the mouse is within the boundaries"""
        (pos_x, pos_y) = pos
        (position_x, position_y) = self.position
        if pos_x >= position_x and (pos_x <= position_x + self.width):
            if pos_y >= position_y and \
                    (pos_y <= position_y + self.height):
                return True
        return False






