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



class BulletSprite(Sprite):
    def __init__(self, center):
        super(BulletSprite, self).__init__()
        self.projectiles = ["Assets/projectile1.png", "Assets/projectile2.png", "Assets/projectile3.png"]
        self.image = pygame.image.load(self.projectiles[0])
        self.animation_id = 0
        self.rect = self.image.get_rect()
        self.rect.center = center

    def animate(self):
        self.animation_id = (self.animation_id+1) % 3

        self.image = pygame.image.load(self.projectiles[self.animation_id])

class Wall(Sprite):
    def __init__(self, loc_x, loc_y):
        super(Wall, self).__init__()
        self.image = pygame.image.load("Assets/wall.png")
        self.rect = self.image.get_rect()
        self.rect.x = loc_x
        self.rect.y = loc_y
