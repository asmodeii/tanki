__author__ = 'Tomasz Rzepka'

import pygame
import sys

class Game:
    def __init__(self, screen, game_data, bg_color=(0, 0, 0)):
        self.screen = screen
        self.bg_color = bg_color
        self.game_data = game_data
        self.clock = pygame.time.Clock()
        self.mouse_is_visible = False
        self.mainloop = False

    def stop(self):
        self.mainloop = False

    def mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def run(self):
        self.mainloop = True
        while self.mainloop:
            self.clock.tick(100)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pass

            self.mouse_visibility()

            pygame.display.flip()
