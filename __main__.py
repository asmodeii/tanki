"""
Main module, runs game
"""
__author__ = 'Pawel Kalecinski, Tomasz Rzepka'

import pygame
import sys
from application import SCREEN_WIDTH, SCREEN_HEIGHT, CONFIGURATION,\
    NewGame, Credits, Settings, GameMenu
pygame.init()

if __name__ == "__main__":

    def _creator():
        """
        function allowing state change of screen to game creation
        """
        screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        game = NewGame(screen2)
        game.run()

    def _credits():
        """
        function allowing state change of screen to credits view
        """
        screen3 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        credits_screen = Credits(screen3)
        credits_screen.run()

    def _settings():
        """
        function allowing state change of screen to settings view
        """
        screen4 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        settings = Settings(screen4)
        settings.run()

    CONFIGURATION.load()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    FUNCS = (("New Game", _creator), ("About", _credits),
             ("Settings", _settings), ("Exit", sys.exit))
    pygame.display.set_caption("PyTank")
    GM = GameMenu(SCREEN, FUNCS)
    GM.run()
