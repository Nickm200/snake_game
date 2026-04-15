import pygame
from settings import *

class Snake:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)]
        self.direction = pygame.Vector2(1, 0)
        self.has_eaten = False
        self.flipped = False

    def update(self):
        if self.has_eaten:
            # grow the snake
            body_copy = self.body[:]
            if self.flipped:
                body_copy.append(body_copy[-1] + self.direction)
            else:
                body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.has_eaten = False
            # flip which end is the head, keep same direction
            self.flipped = not self.flipped
        else:
            # normal movement
            if self.flipped:
                body_copy = self.body[1:]
                body_copy.append(body_copy[-1] + self.direction)
                self.body = body_copy[:]
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]

    def draw(self):
        for point in self.body:
            rect = pygame.Rect(point.x * CELL_SIZE, point.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.display_surface, 'blue', rect)