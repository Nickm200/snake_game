import pygame
from settings import *

class Main:

    def __init__(self):
        #initializes basics of pygame
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.display_surface.fill(LIGHT_GREEN)
            pygame.display.update()
main = Main()
main.run()