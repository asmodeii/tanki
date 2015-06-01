"""settins"""
__author__ = 'Pawel Kalecinski Tomasz Rzepka'

import pygame
from application.KeyConfig import KeyConfig
from application.configs import SCREEN_WIDTH, SCREEN_HEIGHT, CONFIGURATION
from application.state import State

class Settings(State):
    """Settings creator"""
    def __init__(self, screen, bg_color=(0, 0, 0)):
        super(Settings, self).__init__(screen, bg_color)
        funcs = (("Key Configuration", self.key_config),
                 (self.get_bonus_string(), self.toggle_bonus),
                 ("Back", self.stop))
        self.initialize(funcs)

    @staticmethod
    def get_bonus_string():
        """return Bonus:ON or Bonus:OFF"""
        if CONFIGURATION.allow_bonuses:
            return "Bonus: On"
        return "Bonus: Off"

    def toggle_bonus(self):
        """Set allow_bonuses"""
        if CONFIGURATION.allow_bonuses:
            CONFIGURATION.allow_bonuses = False
            self.items[1].text = "Bonus: Off"
        else:
            CONFIGURATION.allow_bonuses = True
            self.items[1].text = "Bonus: On"

    @staticmethod
    def key_config():
        """transition to keyconfig"""
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        kc1 = KeyConfig(screen)
        kc1.run()
