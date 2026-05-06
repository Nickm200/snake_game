import pygame
from settings import *
from random import choice

class Biome:
    BIOMES = {
        "forest": {
            "name": "Forest",
            "light": pygame.Color(170, 215, 81),
            "dark":  pygame.Color(162, 209, 73),
        },
        "desert": {
            "name": "Desert",
            "light": pygame.Color(237, 201, 120),
            "dark":  pygame.Color(220, 180, 90),
        },
        "snow": {
            "name": "Snow",
            "light": pygame.Color(220, 235, 245),
            "dark":  pygame.Color(190, 210, 230),
        },
        "candy land": {
            "name": "Candy Land",
            "light": pygame.Color(248, 215, 228),
            "dark":  pygame.Color(230, 185, 208),
        },
        "pastel": {
            "name": "Sky",
            "light": pygame.Color(135, 185, 230),
            "dark":  pygame.Color(100, 160, 210),
        },
    }

    def __init__(self):
        self.current = self.BIOMES["forest"]  # default
        self.font = pygame.font.SysFont("comicsansms", 18)

    def randomize(self):
        #self.current = choice(list(self.BIOMES.values()))
        choices = [b for b in self.BIOMES.values() if b != self.current]
        self.current = choice(choices)

    @property
    def light(self):
        return self.current["light"]

    @property
    def dark(self):
        return self.current["dark"]

    @property
    def name(self):
        return self.current["name"]

    def draw_label(self, surface):
        surf = self.font.render(f"Biome: {self.name}", True, (255, 255, 255))
        surface.blit(surf, (10, 40))