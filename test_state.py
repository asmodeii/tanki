"""
Tests for State class
"""
__author__ = 'Pawel Kalecinski'

from unittest import TestCase
import pygame
from application.state import State

pygame.init()


class TestSettings(TestCase):
    """
    test state
    """
    def setUp(self):
        """"setUP"""
        self.sup = State((0, 0, 0))
        self.seq = range(0, 300)
        self.seq1 = range(301, 600)
        self.und = range(-100, -1)


    def test_mouse_visible(self):
        """"test function mouse_visible"""
        self.assertTrue(pygame.mouse.set_visible)

    def test_stop(self):
        """"test function stop"""
        self.assertEqual(self.sup.mainloop, False)

    def test_item_selection(self):
        """"test function item_selection"""
        self.assertEqual(self.sup.curr_item, None)
        if self.sup.item_selection(pygame.K_UP):
            self.assertFalse(self.sup.curr_item in self.und)
        elif self.sup.item_selection(pygame.K_DOWN) and \
                        self.sup.curr_item == len(self.sup.items) - 1:
            self.assertEqual(self.sup.curr_item, 0)

    def test_get_input(self):
        """"test function get_input"""
        self.assertTrue(self.sup.mouse_is_visible)
        self.assertEqual(self.sup.curr_item, None)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.assertFalse(self.sup.mouse_is_visible)
