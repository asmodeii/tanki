"""Key Configuration"""
__author__ = 'Pawel Kalecinski'

from application.state import State

class KeyConfig(State):
    """Settings of Key Configuration"""
    def __init__(self, screen, bg_color=(0, 0, 0)):
        super(KeyConfig, self).__init__(screen, bg_color)
        funcs = (("Configuration", "1"), ("Player 1", "2"),
                 ("Player 2", "3"), ("Player 3", "4"),
                 ("Player 4", "5"), ("Back", self.stop))
        self.initialize(funcs)
