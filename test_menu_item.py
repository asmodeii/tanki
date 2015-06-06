"""
Tests for MenuItem class
"""
__author__ = 'Pawel Kalecinski'

from unittest import TestCase
import pygame
from application.menu_item import MenuItem, RED, ORANGE
pygame.init()


class TestMenuItem(TestCase):
    """
    test menu
    """
    def setUp(self):
        self.seq = MenuItem("New Game")
        self.raq = range(0, 300)
        self.raq1 = range(400, 700)

    def test_get_width(self):
        """test function get_width"""
        self.assertTrue(self.seq.get_width() in self.raq)
        self.assertFalse(self.seq.get_width() in self.raq1)

    def test_get_height(self):
        """test function get_height"""
        self.assertTrue(self.seq.get_height() in self.raq)
        self.assertFalse(self.seq.get_height() in self.raq1)

    def test_set_color(self):
        """test function set_color"""
        self.assertEqual(self.seq.font_color, RED)
        if self.seq.is_selected:
            self.assertEqual(self.seq.font_color, ORANGE)

    def test_mouse_selection(self):
        """test function mouse_selection"""
        self.assertFalse(self.seq.mouse_selection((4, 401)))
        self.assertFalse(self.seq.mouse_selection((1000, 100)))
        self.assertFalse(self.seq.mouse_selection((600, 0)))
        self.assertFalse(self.seq.mouse_selection((1200, 750)))
