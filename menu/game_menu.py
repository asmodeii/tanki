__author__ = 'Pawel Kalecinski'

from menu_item import *
from configs import SCREEN_HEIGHT, SCREEN_WIDTH
import sys

class GameMenu:
    def __init__(self, screen, funcs, font='Assets/armalite.ttf', font_size=100,
                 font_color=RED, img='Assets/tanks.jpg'):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_img = pygame.image.load(img)
        self.bg_rect = self.bg_img.get_rect()
        self.clock = pygame.time.Clock()
        self.funcs = funcs
        self.items = []

        for index, item in enumerate(funcs):
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
        mainloop = True
        while mainloop:
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
            self.screen.blit(self.bg_img, ((SCREEN_WIDTH - self.bg_rect.width) / 2,
                                           (SCREEN_HEIGHT - self.bg_rect.height) / 2))

            for item in self.items:
                if self.mouse_is_visible:
                    mouse_pos = pygame.mouse.get_pos()
                    self.mouse_select(item, mouse_pos)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()
