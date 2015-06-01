"""
Module for game configuration
"""
__author__ = 'Tomasz Rzepka'

import pygame
import json

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

class PlayerKeyBindings:
    """
    Key bindings for player
    """
    def __init__(self,
                 up_key=pygame.K_UP, down=pygame.K_DOWN,
                 left=pygame.K_LEFT, right=pygame.K_RIGHT):
        """
        :param up_key: move forward
        :param down: move backward
        :param left: rotate left
        :param right: rotate right
        """
        self.up_key = up_key
        self.down = down
        self.left = left
        self.right = right
        self.action = up_key

    def set_action_key(self, action=pygame.K_SPACE):
        """
        And that proves that 100% PyLint is really really really bad idea
        :param action: fire bullet
        """
        self.action = action

    def get_action_key(self):
        """
        PyLint Love
        :return: action key
        """
        return self.action

class Configuration:
    """
    Base game configuration
    """
    def __init__(self):
        """
        Initializes configuration
        """
        self.player_key_list = []
        self.allow_bonuses = True

    def load(self):
        """
        Loads configuration from settings.json
        """
        json_file = open('settings.json')
        configuration = json.load(json_file)
        self.player_key_list = [PlayerKeyBindings(configuration['p'+str(i)+'keys']['up'],
                                                  configuration['p'+str(i)+'keys']['down'],
                                                  configuration['p'+str(i)+'keys']['left'],
                                                  configuration['p'+str(i)+'keys']['right'])
                                for i in range(4)]
        for i in range(4):
            self.player_key_list[i].set_action_key(configuration['p'+str(i)+'keys']['action'])

    @staticmethod
    def save():
        """
        Saves configuration to settings.json
        :return:
        """
        configuration = {
            'p0keys': {'left': CONFIGURATION.player_key_list[0].left,
                       'right': CONFIGURATION.player_key_list[0].right,
                       'up': CONFIGURATION.player_key_list[0].up_key,
                       'down': CONFIGURATION.player_key_list[0].down,
                       'action': CONFIGURATION.player_key_list[0].action},
            'p1keys': {'left': CONFIGURATION.player_key_list[1].left,
                       'right': CONFIGURATION.player_key_list[1].right,
                       'up': CONFIGURATION.player_key_list[1].up_key,
                       'down': CONFIGURATION.player_key_list[1].down,
                       'action': CONFIGURATION.player_key_list[1].action},
            'p2keys': {'left': CONFIGURATION.player_key_list[2].left,
                       'right': CONFIGURATION.player_key_list[2].right,
                       'up': CONFIGURATION.player_key_list[2].up_key,
                       'down': CONFIGURATION.player_key_list[2].down,
                       'action': CONFIGURATION.player_key_list[2].action},
            'p3keys': {'left': CONFIGURATION.player_key_list[3].left,
                       'right': CONFIGURATION.player_key_list[3].right,
                       'up': CONFIGURATION.player_key_list[3].up_key,
                       'down': CONFIGURATION.player_key_list[3].down,
                       'action': CONFIGURATION.player_key_list[3].action},
        }
        with open('settings.json', 'w') as json_file:
            json.dump(configuration, json_file)

CONFIGURATION = Configuration()
