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
        self.sut.tank.rect.center = (100, 100)

    def test_turn_on(self):
        """
        tests test_turn_on function
        """
        self.assertFalse(self.sut.status['is_on'])
        self.sut.turn_on()
        self.assertTrue(self.sut.status['is_on'])

    def test_turn_off(self):
        """
        tests test_turn_off function
        """
        self.sut.turn_on()
        self.assertTrue(self.sut.status['is_on'])
        self.sut.turn_off()
        self.assertFalse(self.sut.status['is_on'])

    def test_rotate(self):
        """
        tests test_rotate function
        """
        self.assertEquals(self.sut.moving['angle'], 0)
        self.assertTrue(self.sut.rotate(10))
        self.assertEquals(self.sut.moving['angle'], 10)
        self.assertTrue(self.sut.rotate(-30))
        self.assertEquals(self.sut.moving['angle'], -20)

    def test_rotate_collision(self):
        """
        tests test_rotate function for collision
        """
        self.sut.tank.rect.center = (25, 25)
        self.assertEquals(self.sut.moving['angle'], 0)
        self.assertFalse(self.sut.rotate(10))
        self.assertEquals(self.sut.moving['angle'], 0)
        self.assertFalse(self.sut.rotate(-20))
        self.assertEquals(self.sut.moving['angle'], 0)

    def test_rotate_vector(self):
        """
        tests test_rotate_vector function
        """
        self.assertEquals(self.sut.moving['vector'], (0, -1))
        self.assertTrue(self.sut.rotate(10))
        self.sut.rotate_vector()
        (sut_x, sut_y) = self.sut.moving['vector']
        (vec_x, vec_y) = (0.1736, -0.9848)
        self.assertAlmostEquals(sut_x, vec_x, places=4)
        self.assertAlmostEquals(sut_y, vec_y, places=4)
        self.assertTrue(self.sut.rotate(-20))
        self.sut.rotate_vector()
        (sut_x, sut_y) = self.sut.moving['vector']
        (vec_x, vec_y) = (-0.1736, -0.9848)
        self.assertAlmostEquals(sut_x, vec_x, places=4)
        self.assertAlmostEquals(sut_y, vec_y, places=4)

    def test_forward(self):
        """
        tests test_forward function
        """
        self.sut.tank.rect.center = (100, 100)
        self.assertTrue(self.sut.forward())
        self.assertEquals(self.sut.tank.rect.center, (100, 98))
        self.assertTrue(self.sut.forward())
        self.assertEquals(self.sut.tank.rect.center, (100, 96))
        self.assertTrue(self.sut.rotate(-40))
        self.sut.rotate_vector()
        self.assertTrue(self.sut.forward())
        self.assertEquals(self.sut.tank.rect.center, (101, 95))
        self.assertTrue(self.sut.rotate(100))
        self.sut.rotate_vector()
        self.assertTrue(self.sut.forward())
        self.assertEquals(self.sut.tank.rect.center, (100, 94))
        self.sut.tank.rect.center = (25, 25)
        self.assertFalse(self.sut.forward())

    def test_backward(self):
        """
        tests test_backward function
        """
        self.sut.tank.rect.center = (100, 100)
        self.assertTrue(self.sut.backward())
        self.assertEquals(self.sut.tank.rect.center, (100, 102))
        self.assertTrue(self.sut.backward())
        self.assertEquals(self.sut.tank.rect.center, (100, 104))
        self.assertTrue(self.sut.rotate(-40))
        self.sut.rotate_vector()
        self.assertTrue(self.sut.backward())
        self.assertEquals(self.sut.tank.rect.center, (99, 105))
        self.assertTrue(self.sut.rotate(100))
        self.sut.rotate_vector()
        self.assertTrue(self.sut.backward())
        self.assertEquals(self.sut.tank.rect.center, (100, 106))
        self.sut.tank.rect.center = (25, 25)
        self.assertFalse(self.sut.backward())

    def test_set_action_drive(self):
        """
        tests test_set_action_drive function
        """
        self.assertEquals(self.sut.action_drive, self.sut.none_action)
        self.sut.set_action_drive(self.sut.forward)
        self.assertEquals(self.sut.action_drive, self.sut.forward)
        self.sut.set_action_drive(self.sut.backward)
        self.assertEquals(self.sut.action_drive, self.sut.backward)

    def test_set_action_rotate(self):
        """
        tests test_set_action_rotate function
        """
        self.assertEquals(self.sut.action_drive, self.sut.none_action)
        self.sut.set_action_drive(self.sut.rotate)
        self.assertEquals(self.sut.action_drive, self.sut.rotate)

    def test_damage(self):
        """
        tests test_damage function
        """
        health = self.sut.status['health']
        damage = 25
        self.sut.damage(damage)
        self.assertEquals(self.sut.status['health'], health-damage)
