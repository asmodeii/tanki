__author__ = 'Tomasz Rzepka'
import pygame
import math
from pygame.sprite import Sprite

TANKS = ['Assets/tank1.png', 'Assets/tank2.png', 'Assets/tank3.png', 'Assets/tank4.png', 'Assets/enemyTank.png']

class Tank(Sprite):
    def __init__(self, tank_id):
        super(Tank, self).__init__()
        self.tank_id = tank_id
        self.base_image = pygame.image.load(TANKS[tank_id % 5])
        self.image = self.base_image
        self.rect = self.image.get_bounding_rect()

    def change_image(self, tank_id):
        self.tank_id = tank_id % 4
        self.base_image = pygame.image.load(TANKS[tank_id % 5])
        self.image = self.base_image



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
