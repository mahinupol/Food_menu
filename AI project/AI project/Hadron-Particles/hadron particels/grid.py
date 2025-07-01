# grid.py

import pygame

# Constants for grid
GRID_COLOR = (200, 200, 200)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

class Grid:
    def __init__(self, size, cell_size):
        self.size = size
        self.cell_size = cell_size
        self.cells = [[None for _ in range(size)] for _ in range(size)]  # Board initialization

    def draw(self, screen):
        for x in range(0, SCREEN_WIDTH, self.cell_size):
            for y in range(0, SCREEN_HEIGHT, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    def place_tile(self, x, y, color):
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        if self.cells[grid_y][grid_x] is None:
            self.cells[grid_y][grid_x] = color
            return True
        return False

    def draw_tiles(self, screen):
        for y in range(self.size):
            for x in range(self.size):
                if self.cells[y][x] is not None:
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, self.cells[y][x], rect)

    def check_full(self):
        for row in self.cells:
            for cell in row:
                if cell is None:
                    return False
        return True

    def count_tiles(self, color):
        count = 0
        for row in self.cells:
            for cell in row:
                if cell == color:
                    count += 1
        return count
