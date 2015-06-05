"""
Tests for Player class
"""
from unittest import TestCase
import pygame
import application
from game_core.game_data import Player
pygame.init()


__author__ = 'Tomasz Rzepka'


class TestPlayer(TestCase):
    """
    test suite
    """
    def setUp(self):
        """
        setUp fixture
        """
        self.sut = Player(0)

    def test_turn_on(self):
        """
        tests test_turn_on function
        """
        self.assertFalse(self.sut.status['is_on'])
        self.assertFalse(self.sut.tank.is_on)
    #
    # def test_turn_off(self):
    #     """
    #     tests test_turn_off function
    #     """
    #     self.fail()
    #
    # def test_rotate(self):
    #     """
    #     tests test_rotate function
    #     """
    #     self.fail()
    #
    # def test_rotate_vector(self):
    #     """
    #     tests test_rotate_vector function
    #     """
    #     self.fail()
    #
    # def test_forward(self):
    #     """
    #     tests test_forward function
    #     """
    #     self.fail()
    #
    # def test_backward(self):
    #     """
    #     tests test_backward function
    #     """
    #     self.fail()
    #
    # def test_set_action_drive(self):
    #     """
    #     tests test_set_action_drive function
    #     """
    #     self.fail()
    #
    # def test_set_action_rotate(self):
    #     """
    #     tests test_set_action_rotate function
    #     """
    #     self.fail()
    #
    # def test_act(self):
    #     """
    #     tests test_act function
    #     """
    #     self.fail()
    #
    # def test_none_action(self):
    #     """
    #     tests test_none_action function
    #     """
    #     self.fail()
    #
    # def test_fire(self):
    #     """
    #     tests test_fire function
    #     """
    #     self.fail()
    #
    # def test_damage(self):
    #     """
    #     tests test_damage function
    #     """
    #     self.fail()
