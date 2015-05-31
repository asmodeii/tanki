"""
Module for base sprites for agents in game
"""
__author__ = 'Tomasz Rzepka'
import pygame
from pygame.sprite import Sprite

TANKS = ['Assets/tank1.png', 'Assets/tank2.png', 'Assets/tank3.png', 'Assets/tank4.png',
         'Assets/enemyTank.png']

class Tank(Sprite, object):
    """
    Tank Sprite for all tanks in game
    """
    def __init__(self, tank_id, parent):
        """
        :param tank_id: number % available, of image that will represent tank
        :param parent: controller of tank
        """
        super(Tank, self).__init__()
        self.tank_id = tank_id
        self.base_image = pygame.image.load(TANKS[tank_id % 5])
        self.image = self.base_image
        self.rect = self.image.get_bounding_rect()
        self.parent = parent

    def change_image(self, tank_id):
        """
        changes image of tank
        :param tank_id: number % available, of image that will represent tank
        """
        self.tank_id = tank_id % 4
        self.base_image = pygame.image.load(TANKS[tank_id % 5])
        self.image = self.base_image


class HotBulletSprite(Sprite, object):
    """
    Sprite for bullet that deals more damage
    """
    def __init__(self, center):
        """
        :param center: localization of bullet
        """
        super(HotBulletSprite, self).__init__()
        self.image = pygame.image.load("Assets/hot_projectile.png")
        self.rect = self.image.get_rect()
        self.rect.center = center


class BulletSprite(Sprite, object):
    """
    Sprite for standard bullet
    """
    def __init__(self, center):
        """
        :param center: localization of bullet
        """
        super(BulletSprite, self).__init__()
        self.projectiles = ["Assets/projectile1.png",
                            "Assets/projectile2.png",
                            "Assets/projectile3.png"]
        self.image = pygame.image.load(self.projectiles[0])
        self.animation_id = 0
        self.rect = self.image.get_rect()
        self.rect.center = center

    def animate(self):
        """
        Animates bullet
        """
        self.animation_id = (self.animation_id+1) % 3
        self.image = pygame.image.load(self.projectiles[self.animation_id])


class Wall(Sprite, object):
    """
    Sprite for wall (obstacle)
    """
    def __init__(self, loc_x, loc_y):
        """
        :param loc_x: x localization of wall
        :param loc_y: y localization of wall
        """
        super(Wall, self).__init__()
        self.image = pygame.image.load("Assets/wall.png")
        self.rect = self.image.get_rect()
        self.rect.x = loc_x
        self.rect.y = loc_y

class BonusSprite(Sprite, object):
    """
    Sprite for in game bonus
    """
    def __init__(self, bonus_type, center):
        """
        :param bonus_type: bonus type(health - additional health,
                                      damage - increased damage,
                                      speed - increased tank speed,
                                      attack_speed - increased attack speed)
        :param center: localization of bonus
        """
        super(BonusSprite, self).__init__()
        self.bonuses = {'health': "Assets/bonus_health.png",
                        'damage': "Assets/bonus_damage.png",
                        'speed': "Assets/bonus_speed.png",
                        'attack_speed': "Assets/bonus_attack_speed.png"}
        self.image = pygame.image.load(self.bonuses[bonus_type])
        self.rect = self.image.get_rect()
        self.rect.center = center
