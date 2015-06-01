"""Game Menu"""
__author__ = 'Pawel Kalecinski'

from application.state import State

class GameMenu(State):
    """Main Class of Game Menu"""
    def __init__(self, screen, funcs, font_size=100):
        super(GameMenu, self).__init__(screen, bg_image="Assets/tanks.jpg")
        self.initialize(funcs, font_size=font_size)
