__author__ = 'Tomasz Rzepka'

import pygame
import json

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

class PlayerKeyBindings:
    def __init__(self,
                 up=pygame.K_UP, down=pygame.K_DOWN, left=pygame.K_LEFT, right=pygame.K_RIGHT, action=pygame.K_SPACE,):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.action = action

class Configuration:

    def __init__(self):
        self.player_key_list = []

    def load(self): # uzyjcie tej metody gdzies przy uruchamianiu gry
        json_file = open('settings.json')
        configuration = json.load(json_file)
        self.player_key_list = [PlayerKeyBindings(configuration['p'+str(i)+'keys']['action'],
                                                          configuration['p'+str(i)+'keys']['up'],
                                                          configuration['p'+str(i)+'keys']['down'],
                                                          configuration['p'+str(i)+'keys']['left'],
                                                          configuration['p'+str(i)+'keys']['right'])
                                for i in range(4)]  # 4 = max_players, mozecie zmienic

    def save(self):  # uzyjcie tej metody jak bedziecie wracac z opcji
        configuration = { #  zakladam ze zrobicie tak ze zmiana 1 przycisku w opcjach zmieni odp. czesc config
            'p0keys': {'left': config.player_key_list[0].left,
                       'right': config.player_key_list[0].right,
                       'up': config.player_key_list[0].up,
                       'down': config.player_key_list[0].down,
                       'action': config.player_key_list[0].action},
            'p1keys': {'left': config.player_key_list[1].left,
                       'right': config.player_key_list[1].right,
                       'up': config.player_key_list[1].up,
                       'down': config.player_key_list[1].down,
                       'action': config.player_key_list[1].action},
            'p2keys': {'left': config.player_key_list[2].left,
                       'right': config.player_key_list[2].right,
                       'up': config.player_key_list[2].up,
                       'down': config.player_key_list[2].down,
                       'action': config.player_key_list[2].action},
            'p3keys': {'left': config.player_key_list[3].left,
                       'right': config.player_key_list[3].right,
                       'up': config.player_key_list[3].up,
                       'down': config.player_key_list[3].down,
                       'action': config.player_key_list[3].action},
        }
        with open('configuration.json', 'w') as json_file:
                json.dump(configuration, json_file)

config = Configuration()
