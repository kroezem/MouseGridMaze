import numpy as np
import gymnasium as gym
import pygame
import colorsys


class Mouse:
    def __init__(self, maze):
        super().__init__()

        self.maze = maze
        self.position = self.maze.start
        self.visited = np.zeros_like(self.maze.array, dtype=np.int16)

        # OBSERVATION SHAPE EXTREMELY IMPORTANT
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(8,), dtype=np.uint8)

    def observe(self):
        self.visited[self.position] += 1

        row, col = self.position
        max_row, max_col = self.maze.array.shape

        def get_value(array, r, c, default=255):
            if 0 <= r < max_row and 0 <= c < max_col:
                return array[r, c]
            return default

        obs = [
            get_value(self.maze.array, row - 1, col),  # Top
            get_value(self.maze.array, row + 1, col),  # Bottom
            get_value(self.maze.array, row, col - 1),  # Left
            get_value(self.maze.array, row, col + 1),  # Right
            get_value(self.visited, row - 1, col),  # Top visited
            get_value(self.visited, row + 1, col),  # Bottom visited
            get_value(self.visited, row, col - 1),  # Left visited
            get_value(self.visited, row, col + 1)  # Right visited
        ]

        return obs

    def reward(self, action, step, won):
        reward = 0
        terminated = False
        truncated = False

        if won:
            reward += 100
            terminated = True

        visits = self.visited[self.position]
        if visits == 0:
            reward += 1
        elif visits >= 255:
            truncated = True
        # else:
        #     reward -= 1

        return reward, terminated, truncated

    def draw(self, screen, size=50):
        for row in range(16):
            for col in range(16):
                visits = self.visited[row, col]
                if visits:
                    x = col * size
                    y = row * size
                    # hue = (visits * 10) % 360 / 360.0  # Normalize hue to [0, 1]
                    # color = colorsys.hsv_to_rgb(hue, 1, 1)  # Full saturation and value
                    # color = tuple(int(c * 255) for c in color)  # Convert to [0, 255] range
                    # print(visits)
                    color = (min(visits * 10, 255), 0, max(0, 255 - (visits * 10)))  # THIS IS THE COLOR GRADIENT
                    pygame.draw.rect(screen, color, (x, y, size, size))

        original_image = pygame.image.load('mouse.png')
        image = pygame.transform.scale(original_image, (size, size))

        # Calculate the top-left position for the mouse image
        x, y = self.position[1] * size, self.position[0] * size

        # Draw the mouse image on the screen
        screen.blit(image, (x, y))
