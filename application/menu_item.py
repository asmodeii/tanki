"""Menu Items"""
__author__ = 'Pawel Kalecinski'
import pygame


RED = (255, 0, 0)
ORANGE = (255, 180, 0)

class MenuItem(pygame.font.Font, object):
    """Creating Menu Items"""
    def __init__(self, text, font=None, font_params=(RED, 30), position=(0, 0)):
        (self.font_color, font_size) = font_params
        super(MenuItem, self).__init__(font, font_size)
        self.text = text
        self.base_font_color = self.font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.position = position
        self.is_selected = False
        self.func = None

    def get_width(self):
        """
        :return: text width
        """
        return self.label.get_rect().width

    def get_height(self):
        """
        :return: text height
        """
        return self.label.get_rect().height

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
        if pos_x >= position_x and (pos_x <= position_x + self.get_width()):
            if pos_y >= position_y and \
                    (pos_y <= position_y + self.get_height()):
                return True
        return False
