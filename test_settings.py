__author__ = 'Pawel Kalecinski'

from unittest import TestCase
import pygame
from application.configs import CONFIGURATION
from application.settings import Settings
pygame.init()


class TestSettings(TestCase):

    def test_get_bonus_string(self):
        if CONFIGURATION.allow_bonuses:
            self.assertEqual(Settings.get_bonus_string(), 'Bonus: On')
        else:
            self.assertEqual(Settings.get_bonus_string(), 'Bonus: Off')

    def test_toggle_bonus(self):
        if CONFIGURATION.allow_bonuses:
            self.assertEqual(CONFIGURATION.allow_bonuses, True)
        else:
            self.assertEqual(CONFIGURATION.allow_bonuses, False)
