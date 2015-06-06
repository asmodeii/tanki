"""
Tests for Settings class
"""
__author__ = 'Pawel Kalecinski'

from unittest import TestCase
import pygame
from application.configs import CONFIGURATION
from application.settings import Settings
pygame.init()


class TestSettings(TestCase):
    """
    test settings
    """
    def test_get_bonus_string(self):
        """test function get_bonus_string"""
        if CONFIGURATION.allow_bonuses:
            self.assertEqual(Settings.get_bonus_string(), 'Bonus: On')
        else:
            self.assertEqual(Settings.get_bonus_string(), 'Bonus: Off')

    def test_toggle_bonus(self):
        """"test function toggle_bonus"""
        if CONFIGURATION.allow_bonuses:
            self.assertEqual(CONFIGURATION.allow_bonuses, True)
        else:
            self.assertEqual(CONFIGURATION.allow_bonuses, False)
