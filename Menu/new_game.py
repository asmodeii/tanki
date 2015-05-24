__author__ = 'Tomasz Rzepka, Pawel Kalecinski'

from game_menu import GameMenu
import pygame
from menu_item import RED, ORANGE, MenuItem

class NewGame:
    def __init__(self, screen, bg_color=(0, 0, 0)):
        self.screen = screen
        self.bg_color = bg_color
        self.img = pygame.image.load("Assets/tanks2.jpg")
        font='Assets/armalite.ttf'
        font_size=50
        font_color=RED
        self.funcs = (("Player <1>", None), ("About", None), ("Settings", None), ("Back", self.stop))
        self.mainloop = False
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.mainloop = False
        self.items = []
        self.clock = pygame.time.Clock()

        for index, item in enumerate(self.funcs):
            (key, func) = item
            menu_item = MenuItem(key, font, font_size, font_color)
            height_text = len(self.funcs) * menu_item.height
            position_x = (self.scr_width / 2) - (menu_item.width / 2)
            position_y = (self.scr_height / 2) - (height_text / 2) + \
                         ((index * 2) + index * menu_item.height)
            menu_item.set_position(position_x, position_y)
            menu_item.func = func
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def stop(self):
        self.mainloop=False

    def mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def item_selection(self, key):
        for item in self.items:
            item.set_italic(False)
            item.set_color(RED)

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
                self.mainloop = False

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_color(ORANGE)

        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            self.items[self.cur_item].func()

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
                    self.mainloop = False
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
            self.screen.blit(self.img, (0, 0))

            for item in self.items:
                if self.mouse_is_visible:
                    mouse_pos = pygame.mouse.get_pos()
                    self.mouse_select(item, mouse_pos)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()
