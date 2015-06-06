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
        """"setUP"""
        self.seq = MenuItem("New Game")
        self.seq1 = MenuItem("Settings")
        self.seq2 = MenuItem("Exit")
        self.raq = range(0, 300)
        self.raq1 = range(400, 700)

    def test_get_width(self):
        """test function get_width"""
        self.assertTrue(self.seq.get_width() in self.raq)
        self.assertFalse(self.seq.get_width() in self.raq1)
        self.assertTrue(self.seq1.get_width() in self.raq)
        self.assertFalse(self.seq1.get_width() in self.raq1)
        self.assertTrue(self.seq2.get_width() in self.raq)
        self.assertFalse(self.seq2.get_width() in self.raq1)

    def test_get_height(self):
        """test function get_height"""
        self.assertTrue(self.seq.get_height() in self.raq)
        self.assertFalse(self.seq.get_height() in self.raq1)
        self.assertTrue(self.seq1.get_height() in self.raq)
        self.assertFalse(self.seq1.get_height() in self.raq1)
        self.assertTrue(self.seq2.get_height() in self.raq)
        self.assertFalse(self.seq2.get_height() in self.raq1)

    def test_set_color(self):
        """test function set_color"""
        self.assertEqual(self.seq.font_color, RED)
        if self.seq.is_selected:
            self.assertEqual(self.seq.font_color, ORANGE)

        self.assertEqual(self.seq2.font_color, RED)
        if self.seq2.is_selected:
            self.assertEqual(self.seq2.font_color, ORANGE)


    def test_mouse_selection(self):
        """test function mouse_selection"""
        self.assertFalse(self.seq.mouse_selection((4, 401)))
        self.assertFalse(self.seq.mouse_selection((1000, 100)))
        self.assertFalse(self.seq.mouse_selection((600, 0)))
        self.assertFalse(self.seq.mouse_selection((1200, 750)))
        self.assertFalse(self.seq1.mouse_selection((0, 421)))
        self.assertFalse(self.seq1.mouse_selection((199, 100)))
        self.assertFalse(self.seq1.mouse_selection((630, 0)))
        self.assertFalse(self.seq1.mouse_selection((1200, 750)))
        self.assertFalse(self.seq2.mouse_selection((40, 41)))
        self.assertFalse(self.seq2.mouse_selection((100, 100)))
        self.assertFalse(self.seq2.mouse_selection((604, 10)))
        self.assertFalse(self.seq2.mouse_selection((1200, 750)))
