__author__ = 'Tomasz Rzepka'
import pygame
import math
from pygame.sprite import Sprite

TANKS = ['Assets/tank1.png', 'Assets/tank2.png', 'Assets/tank3.png', 'Assets/tank4.png', 'Assets/enemyTank.png']

class Tank(Sprite):
    def __init__(self, tank_id):
        super(Tank, self).__init__()
        self.angle = 0
        self.vector = (0.0, -1.0)
        self.position_debt = (0.0, 0.0)
        self.tank_id = tank_id
        self.is_on = False
        self.action_drive = self.none_action
        self.action_rotate = self.none_action
        #self.sprite = pygame.Surface((50, 50))
        self._image = pygame.image.load(TANKS[tank_id % 5])
        self.image = self._image
        self.rect = self.image.get_rect()

    def set_action_drive(self, action):
        self.action_drive = action

    def set_action_rotate(self, action):
        self.action_rotate = action

    def act(self):
        if self.is_on:
            self.action_rotate()
            self.action_drive()

    def none_action(self):
        pass

    def change_image(self, tank_id):
        self.tank_id = tank_id % 4
        self._image = pygame.image.load(TANKS[tank_id % 5])
        self.image = self._image

    def rotate(self, angle):
        """rotate an image while keeping its center and size"""
        self.angle += angle
        self.rotate_vector()
        orig_rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self._image, self.angle)
        rot_rect = self.rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image

    def rotate_vector(self):
        """Rotate a vector `v` by the given angle, relative to the anchor point."""
        x, y = (0.0, -1.0)
        rad = math.radians(self.angle)
        cos_theta = math.cos(rad)
        sin_theta = math.sin(rad)

        nx = x*cos_theta - y*sin_theta
        ny = x*sin_theta + y*cos_theta
        self.vector = (nx, ny)

    def forward(self):
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y+debt_y)
        self.rect.x -= integral_x
        self.rect.y += integral_y
        self.position_debt = (fractional_x, fractional_y)

    def backward(self):
        (vec_x, vec_y) = self.vector
        (debt_x, debt_y) = self.position_debt
        (fractional_x, integral_x) = math.modf(vec_x+debt_x)
        (fractional_y, integral_y) = math.modf(vec_y+debt_y)
        self.rect.x += integral_x
        self.rect.y -= integral_y
        self.position_debt = (fractional_x, fractional_y)


class Bullet(Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.angle = 0
        self.vector = (0.0, -1.0)
        self.position_debt = (0.0, 0.0)
        #self.sprite = pygame.Surface((10, 10))
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

class Wall(Sprite):
    def __init__(self, loc_x, loc_y):
        super(Wall, self).__init__()
        self.image = pygame.image.load("Assets/wall.png")
        self.rect = self.image.get_rect()
        self.rect.x = loc_x
        self.rect.y = loc_y
