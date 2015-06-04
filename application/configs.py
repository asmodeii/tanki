"""
Module for game configuration
"""
__author__ = 'Tomasz Rzepka'

import json

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

class Configuration(object):
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
        self.player_key_list = [{'up': configuration['p'+str(i)+'keys']['up'],
                                 'down': configuration['p'+str(i)+'keys']['down'],
                                 'left': configuration['p'+str(i)+'keys']['left'],
                                 'right': configuration['p'+str(i)+'keys']['right'],
                                 'action': configuration['p'+str(i)+'keys']['action']}
                                for i in range(4)]

    @staticmethod
    def save():
        """
        Saves configuration to settings.json
        :return:
        """
        configuration = {
            'p0keys': {'left': CONFIGURATION.player_key_list[0]['left'],
                       'right': CONFIGURATION.player_key_list[0]['right'],
                       'up': CONFIGURATION.player_key_list[0]['up'],
                       'down': CONFIGURATION.player_key_list[0]['down'],
                       'action': CONFIGURATION.player_key_list[0]['action']},
            'p1keys': {'left': CONFIGURATION.player_key_list[1]['left'],
                       'right': CONFIGURATION.player_key_list[1]['right'],
                       'up': CONFIGURATION.player_key_list[1]['up'],
                       'down': CONFIGURATION.player_key_list[1]['down'],
                       'action': CONFIGURATION.player_key_list[1]['action']},
            'p2keys': {'left': CONFIGURATION.player_key_list[2]['left'],
                       'right': CONFIGURATION.player_key_list[2]['right'],
                       'up': CONFIGURATION.player_key_list[2]['up'],
                       'down': CONFIGURATION.player_key_list[2]['down'],
                       'action': CONFIGURATION.player_key_list[2]['action']},
            'p3keys': {'left': CONFIGURATION.player_key_list[3]['left'],
                       'right': CONFIGURATION.player_key_list[3]['right'],
                       'up': CONFIGURATION.player_key_list[3]['up'],
                       'down': CONFIGURATION.player_key_list[3]['down'],
                       'action': CONFIGURATION.player_key_list[3]['action']},
        }
        with open('settings.json', 'w') as json_file:
            json.dump(configuration, json_file)

CONFIGURATION = Configuration()
