import pygame
#help us exit game when done
from sys import exit
#import images
from os.path import join



#screen
CELL_SIZE = 80
ROWS = 10
COLS = 16

WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

#colors
LIGHT_GREEN = pygame.Color(170, 215, 81)
DARK_GREEN = pygame.Color(162, 209, 73)


# start position
START_LENGTH = 3
START_ROW = ROW = ROWS // 2
START_COL = START_LENGTH + 2

#shadow
SHADOW_SIZE = pygame.Vector2(4,4)
SHADOW_OPACITY = 50






