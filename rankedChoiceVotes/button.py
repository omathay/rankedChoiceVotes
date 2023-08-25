"""
button.py
author: Owen Mathay
"""

import pygame


class Button:
    norm_color = (125, 99, 2)
    hover_color = (100, 85, 0)

    def __init__(self, name: str, x: int, y: int):
        self.x = x
        self.y = y
        self.name = name
        if self.name == 'info' or self.name == 'back':
            self.size = (50, 50)
        else:
            self.size = (150, 50)
        self.rect = pygame.Rect((x, y), self.size)
        self.color = self.norm_color

    def hover(self, coor: tuple):
        if self.x <= coor[0] <= self.x + self.size[0] and self.y <= coor[1] <= self.y + self.size[1]:
            self.color = self.hover_color
            return True
        else:
            self.color = self.norm_color
            return False