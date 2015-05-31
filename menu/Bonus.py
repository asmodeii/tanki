__author__ = 'Pawel Kalecinski'


import sys
import pygame
from menu_item import RED, ORANGE, MenuItem
from configs import config

GREEN = (80, 240, 120)

class Bonus:
    def __init__(self, screen, bg_color=(0, 0, 0)):
        self.screen = screen
        self.bg_color = bg_color
        self.mouse_is_visible = True
        font = 'Assets/armalite.ttf'
        font_size = 50
        self.font_color = RED
        self.items = []
        self.clock = pygame.time.Clock()
        self.funcs = (("On", self.turnOn), ("Off", self.turnOff), ("Back", self.stop))
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        for index, item in enumerate(self.funcs):
            (key, func) = item
            menu_item = MenuItem(key, font, font_size, self.font_color)
            height_text = len(self.funcs) * menu_item.height
            position_x = (self.scr_width / 2) - (menu_item.width / 2)
            position_y = 0
            if index == 0:
                position_y -= 30
            if index == len(self.funcs) - 1:
                position_y += 30
            position_y += (self.scr_height / 2) - (height_text / 2) + \
                          ((index * 2) + index * menu_item.height)
            menu_item.set_position(position_x, position_y)
            menu_item.func = func
            self.items.append(menu_item)

            self.mouse_is_visible = True
            self.cur_item = None

    def turnOn(self):
        config.allow_bonuses = True

    def turnOff(self):
        config.allow_bonuses = False

    def stop(self):
        self.screen.fill((0, 0, 0))
        self.mainloop = False

    def mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def item_selection(self, key):
        for item in self.items:
            item.set_italic(False)
            item.set_color(self.font_color)

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

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_color(ORANGE)

        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            self.items[self.cur_item].func()

        if config.allow_bonuses == True and (self.cur_item == 0 and \
                        key == pygame.K_RETURN or key == pygame.MOUSEBUTTONDOWN):
            self.items[self.cur_item].set_italic(True)
            self.items[self.cur_item].set_color(GREEN)

        elif config.allow_bonuses == False and (self.cur_item == 1 and \
                        key == pygame.K_RETURN or key == pygame.MOUSEBUTTONDOWN):
            self.items[self.cur_item].set_italic(True)
            self.items[self.cur_item].set_color(GREEN)

    @staticmethod
    def mouse_select(item, mouse_pos):
        if item.mouse_selection(mouse_pos):
            item.set_color(ORANGE)
            item.set_italic(True)
        else:
            item.set_color(RED)
            item.set_italic(False)

    def run(self):
        self.mainloop = True
        while self.mainloop:
            self.clock.tick(100)
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
            self.screen.fill((0, 0, 0))

            for item in self.items:
                if self.mouse_is_visible:
                    mouse_pos = pygame.mouse.get_pos()
                    self.mouse_select(item, mouse_pos)
                self.screen.blit(item.label, item.position)
            pygame.display.flip()
