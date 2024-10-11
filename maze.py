import numpy as np
import pygame

WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Maze:
    def __init__(self, map_file, size=50, stroke=2):

        self.array = np.zeros((16, 16), np.int8)
        self.start = (-1, -1)
        self.goal = (-1, -1)

        lines = open(map_file).read().split('\n')
        for row in range(16):
            for col in range(16):
                # Determine the walls for the current cell
                walls = 0

                if lines[row * 2][col * 4 + 1] == '-':
                    walls |= 1  # Top wall
                if lines[row * 2 + 2][col * 4 + 1] == '-':
                    walls |= 2  # Bottom wall
                if lines[row * 2 + 1][col * 4] == '|':
                    walls |= 4  # Left wall
                if lines[row * 2 + 1][col * 4 + 4] == '|':
                    walls |= 8  # Right wall

                if lines[row * 2 + 1][col * 4 + 2] == 'S':
                    walls |= 16  # Goal
                    self.start = (row, col)
                if lines[row * 2 + 1][col * 4 + 2] == 'G':
                    walls |= 32  # Goal
                    self.goal = (row, col)

                self.array[row, col] = walls

        if self.start == (-1, -1):
            raise ValueError('NO START CELL')
        if self.goal == (-1, -1):
            raise ValueError('NO GOAL CELL')

    def draw(self, screen, size=50, stroke=2):
        for row in range(16):
            for col in range(16):
                walls = self.array[row, col]
                x = col * size
                y = row * size

                if walls & 32:  # Goal
                    original_image = pygame.image.load('cheese.png')
                    image = pygame.transform.scale(original_image, (size, size))
                    screen.blit(image, (x, y))

                if walls & 1:  # Top wall
                    pygame.draw.line(screen, WHITE, (x, y), (x + size, y), stroke)
                if walls & 2:  # Bottom wall
                    pygame.draw.line(screen, WHITE, (x, y + size), (x + size, y + size), stroke)
                if walls & 4:  # Left wall
                    pygame.draw.line(screen, WHITE, (x, y), (x, y + size), stroke)
                if walls & 8:  # Right wall
                    pygame.draw.line(screen, WHITE, (x + size, y), (x + size, y + size), stroke)
