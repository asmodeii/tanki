"""Key Configuration"""
__author__ = 'Pawel Kalecinski, Tomasz Rzepka'

from application.state import State
import pygame
import sys
from application.configs import CONFIGURATION


class KeyConfig(State):
    """Settings of Key Configuration"""
    def __init__(self, screen, bg_color=(0, 0, 0)):
        super(KeyConfig, self).__init__(screen, bg_color)
        self.actual_player = 0
        self.actual_key = False
        funcs = (('Player <%d> keys' % (self.actual_player + 1),
                             self.select_player),
                            ('ACTION: ' + pygame.key.name\
                                (CONFIGURATION.player_key_list\
                                    [self.actual_player]['action']), \
                             self.prepare_key),
                            ('UP: ' + pygame.key.name\
                                (CONFIGURATION.player_key_list\
                                    [self.actual_player]['up']),\
                             self.prepare_key),
                            ('DOWN: ' + pygame.key.name\
                                (CONFIGURATION.player_key_list\
                                    [self.actual_player]['down']),\
                             self.prepare_key),
                            ('LEFT: ' + pygame.key.name\
                                (CONFIGURATION.player_key_list\
                                    [self.actual_player]['left']),\
                             self.prepare_key),
                            ('RIGHT: ' + pygame.key.name\
                                (CONFIGURATION.player_key_list\
                                    [self.actual_player]['right']),\
                             self.prepare_key),
                            ('BACK', self.stop))
        self.initialize(funcs)

    def set_key(self, key):
        """ sets new key"""
        if self.cur_item == 1:
            CONFIGURATION.player_key_list[self.actual_player]['action'] = key
        elif self.cur_item == 2:
            CONFIGURATION.player_key_list[self.actual_player]['up'] = key
        elif self.cur_item == 3:
            CONFIGURATION.player_key_list[self.actual_player]['down'] = key
        elif self.cur_item == 4:
            CONFIGURATION.player_key_list[self.actual_player]['left'] = key
        else:
            CONFIGURATION.player_key_list[self.actual_player]['right'] = key
        self.save_keys()

    def save_keys(self):
        """ save keys"""
        self.items[1].text = 'ACTION: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.actual_player]['action'])
        self.items[2].text = 'UP: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.actual_player]['up'])
        self.items[3].text = 'DOWN: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.actual_player]['down'])
        self.items[4].text = 'LEFT: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.actual_player]['left'])
        self.items[5].text = 'RIGHT: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.actual_player]['right'])

    def prepare_key(self):
        """ Prepares key for new set"""
        self.items[self.cur_item].text = \
            self.items[self.cur_item].text.rsplit(':', 1)[0]
        self.items[self.cur_item].text += ": <Press Key>"
        self.actual_key = True

    def select_player(self):
        """ selects next player"""
        self.actual_player = (
            (self.actual_player + 1) % 4)
        self.items[self.cur_item].text = "Player <%d> keys" % (
            self.actual_player + 1)
        self.save_keys()

    def get_input(self):
        """
        Takes input from player
        """
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.actual_key:
                    self.set_key(event.key)
                    self.actual_key = False
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

