"""
Module for base screen state
"""
__author__ = 'Tomasz Rzepka'

import pygame
import sys
from menu.menu_item import RED, ORANGE, MenuItem
from menu.configs import SCREEN_WIDTH, SCREEN_HEIGHT

class State(object):
    """
    Game creation screen state.
    """
    def __init__(self, screen, bg_color=(0, 0, 0), bg_image=None):
        """
        Generates initial screen
        :param screen: PyGame screen to write on
        :param bg_color: background color
        """
        self.screen = screen
        self.bg_color = bg_color
        if bg_image is None:
            self.bg_img = None
        else:
            self.bg_img = pygame.image.load("Assets/tanks2.jpg")
        self.mainloop = False
        self.items = []
        self.mouse_is_visible = True
        self.cur_item = None

    def initialize(self, funcs=None, font='Assets/armalite.ttf',
                   font_size=50, font_color=RED):
        """
        Initializes item list
        :param funcs: funcs to be created in screen
        """
        scr_width = self.screen.get_rect().width
        scr_height = self.screen.get_rect().height
        if funcs is None:
            funcs = []
        for index, item in enumerate(funcs):
            (key, func) = item
            menu_item = MenuItem(key, font, font_size, font_color)
            height_text = len(funcs) * menu_item.height
            position_x = (scr_width / 2) - (menu_item.width / 2)
            position_y = 0
            if index == 0:
                position_y -= 30
            if index == len(funcs) - 1:
                position_y += 30
            position_y += (scr_height / 2) - (height_text / 2) + \
                          ((index * 2) + index * menu_item.height)
            menu_item.set_position(position_x, position_y)
            menu_item.func = func
            self.items.append(menu_item)

    def stop(self):
        """
        Stops state and returns to previous one
        """
        self.screen.fill((0, 0, 0))
        self.mainloop = False

    def mouse_visibility(self):
        """
        Sets if mouse should be visible
        """
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def item_selection(self, key):
        """
        Interprets user actions
        :param key: key to be interpreted
        """
        for item in self.items:
            item.set_italic(False)
            item.set_color(item.base_font_color)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0
            elif key == pygame.K_ESCAPE:
                self.stop()
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                self.items[self.cur_item].func()

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_color(ORANGE)

    @staticmethod
    def mouse_select(item, mouse_pos):
        """
        Checks if mouse hovers over item
        :param item: item to be checked
        :param mouse_pos: mouse position
        :return:
        """
        if item.mouse_selection(mouse_pos):
            item.set_color(ORANGE)
            item.set_italic(True)
        else:
            item.set_color(RED)
            item.set_italic(False)

    def run(self):
        """
        Base loop for state
        """
        if self.bg_img is not None:
            bg_rect = self.bg_img.get_rect()
        clock = pygame.time.Clock()
        self.mainloop = True
        while self.mainloop:
            self.screen.fill(self.bg_color)
            clock.tick(100)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.item_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.mouse_selection(mouse_pos):
                            item.func()

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.mouse_visibility()
            if self.bg_img is not None:
                self.screen.blit(self.bg_img, ((SCREEN_WIDTH - bg_rect.width) / 2,
                                               (SCREEN_HEIGHT - bg_rect.height) / 2))

            for item in self.items:
                if self.mouse_is_visible:
                    mouse_pos = pygame.mouse.get_pos()
                    self.mouse_select(item, mouse_pos)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()
