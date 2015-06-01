"""Credits"""
__author__ = 'Pawel Kalecinski'

import pygame

class Credits(object):
    """Class contains credits"""
    def __init__(self, screen, bg_color=(0, 0, 0)):
        self.screen = screen
        self.bg_color = bg_color

    def show_text(self):
        """show credits"""
        font = pygame.font.Font('Assets/armalite.ttf', 60)
        text = font.render("Pawel Kalecinski", 1, (255, 255, 255))
        text2 = font.render("Tomasz Rzepka", 1, (255, 255, 255))
        text3 = font.render("2015", 1, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        self.screen.blit(text2, (100, 200))
        self.screen.blit(text3, (100, 300))

    def run(self):
        """mainloop"""
        mainloop = True
        while mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                        or event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                    mainloop = False
            self.screen.fill(self.bg_color)
            self.show_text()
            pygame.display.flip()
