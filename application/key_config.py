"""Key Configuration"""
__author__ = 'Pawel Kalecinski, Tomasz Rzepka'

from application.state import State
import pygame
import sys
from application.configs import CONFIGURATION
from functools import partial

class KeyConfig(State):
    """Settings of Key Configuration"""
    def __init__(self, screen, bg_color=(0, 0, 0)):
        super(KeyConfig, self).__init__(screen, bg_color)
        self.current_player = 0
        self.mouse_is_visible = False
        self.change_key = False
        funcs = (('Player <%d> keys' % (self.current_player + 1), self.select_player),
                 ('ACTION: ' +
                  pygame.key.name(CONFIGURATION.player_key_list[self.current_player]['action']),
                  partial(self.prepare_key, 1)),
                 ('UP: ' +
                  pygame.key.name(CONFIGURATION.player_key_list[self.current_player]['up']),
                  partial(self.prepare_key, 2)),
                 ('DOWN: ' +
                  pygame.key.name(CONFIGURATION.player_key_list[self.current_player]['down']),
                  partial(self.prepare_key, 3)),
                 ('LEFT: ' +
                  pygame.key.name(CONFIGURATION.player_key_list[self.current_player]['left']),
                  partial(self.prepare_key, 4)),
                 ('RIGHT: ' +
                  pygame.key.name(CONFIGURATION.player_key_list[self.current_player]['right']),
                  partial(self.prepare_key, 5)),
                 ('BACK', self.stop))
        self.initialize(funcs)

    def set_key(self, key):
        """ sets new key"""
        if self.curr_item == 1:
            CONFIGURATION.player_key_list[self.current_player]['action'] = key
        elif self.curr_item == 2:
            CONFIGURATION.player_key_list[self.current_player]['up'] = key
        elif self.curr_item == 3:
            CONFIGURATION.player_key_list[self.current_player]['down'] = key
        elif self.curr_item == 4:
            CONFIGURATION.player_key_list[self.current_player]['left'] = key
        elif self.curr_item == 5:
            CONFIGURATION.player_key_list[self.current_player]['right'] = key
        self.save_keys()

    def stop(self):
        CONFIGURATION.save()
        super(KeyConfig, self).stop()

    def save_keys(self):
        """ save keys"""
        self.items[1].text = 'ACTION: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.current_player]['action'])
        self.items[2].text = 'UP: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.current_player]['up'])
        self.items[3].text = 'DOWN: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.current_player]['down'])
        self.items[4].text = 'LEFT: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.current_player]['left'])
        self.items[5].text = 'RIGHT: ' + pygame.key.name(
            CONFIGURATION.player_key_list[self.current_player]['right'])

    def prepare_key(self, item_id):
        """ Prepares key for new set"""
        self.items[item_id].text = self.items[item_id].text.rsplit(':', 1)[0]
        self.items[item_id].text += ": <Press Key>"
        self.change_key = True

    def select_player(self):
        """ selects next player"""
        self.current_player = (
            (self.current_player + 1) % 4)
        self.items[0].text = "Player <%d> keys" % (
            self.current_player + 1)
        self.save_keys()

    def get_input(self):
        """
        Takes input from player
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.change_key:
                    self.set_key(event.key)
                    self.change_key = False
                else:
                    self.item_selection(event.key)
            elif event.type == pygame.QUIT:
                sys.exit()
