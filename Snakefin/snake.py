import pygame
from settings import *

class Snake:
    def __init__(self, double_headed=False):
        self.display_surface = pygame.display.get_surface()
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)]
        self.direction = pygame.Vector2(1, 0)
        self.has_eaten = False
        self.flipped = False
        self.double_headed = double_headed

    def get_head(self):
        return self.body[-1] if self.flipped else self.body[0]

    def get_body_without_head(self):
        return self.body[:-1] if self.flipped else self.body[1:]

    def point_away_from_neck(self):
        # After switching heads, choose the direction that moves away
        # from the body segment next to the new active head.
        if len(self.body) < 2:
            return

        if self.flipped:
            head = self.body[-1]
            neck = self.body[-2]
        else:
            head = self.body[0]
            neck = self.body[1]

        self.direction = head - neck

    def update(self):
        if self.flipped:
            new_head = self.body[-1] + self.direction

            if self.has_eaten:
                self.body.append(new_head)
                self.has_eaten = False

                if self.double_headed:
                    self.flipped = not self.flipped
                    self.point_away_from_neck()
            else:
                self.body = self.body[1:] + [new_head]

        else:
            new_head = self.body[0] + self.direction

            if self.has_eaten:
                self.body.insert(0, new_head)
                self.has_eaten = False

                if self.double_headed:
                    self.flipped = not self.flipped
                    self.point_away_from_neck()
            else:
                self.body = [new_head] + self.body[:-1]

    def draw(self):
        for point in self.body:
            rect = pygame.Rect(point.x * CELL_SIZE, point.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.display_surface, 'blue', rect)

        head = self.get_head()
        rect = pygame.Rect(head.x * CELL_SIZE, head.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.display_surface, 'darkblue', rect)
