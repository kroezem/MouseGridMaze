import os
import random
import time

import numpy as np
import pygame
import gymnasium as gym

from maze import Maze
from mouse import Mouse


class MazeEnv(gym.Env):
    def __init__(self, maze_dir, render_mode="rgb_array", max_steps=5000):
        super(MazeEnv, self).__init__()
        self.max_steps = max_steps
        self.steps = 0

        self.mazes = [os.path.join(maze_dir, f) for f in os.listdir(maze_dir)]

        self.maze = Maze(random.choice(self.mazes))
        self.mouse = Mouse(self.maze)

        # DEFINING THESE SPACES IS EXTREMELY IMPORTANT
        self.action_space = gym.spaces.MultiBinary(4)
        self.observation_space = self.mouse.observation_space

        # SETTING UP PYGAME
        if render_mode == 'human':
            pygame.init()
            self.screen = pygame.display.set_mode((802, 802))
            pygame.display.set_caption("Maze Gym Environment")
            self.clock = pygame.time.Clock()

    def reset(self, seed=None, options=None):
        """RESETS ENV BACK TO BASE STATE"""
        self.maze = Maze(random.choice(self.mazes))
        self.mouse = Mouse(self.maze)
        observation = self.mouse.observe()
        return observation, {}

    def step(self, action):

        cell = self.maze.array[self.mouse.position]

        if action[0] and not cell & 1:  # Up key and no top wall
            self.mouse.position = (self.mouse.position[0] - 1, self.mouse.position[1])
        elif action[1] and not cell & 2:  # Down key and no bottom wall
            self.mouse.position = (self.mouse.position[0] + 1, self.mouse.position[1])
        elif action[2] and not cell & 4:  # Left key and no left wall
            self.mouse.position = (self.mouse.position[0], self.mouse.position[1] - 1)
        elif action[3] and not cell & 8:  # Right key and no right wall
            self.mouse.position = (self.mouse.position[0], self.mouse.position[1] + 1)

        won = self.maze.array[self.mouse.position] & 32

        reward, terminated, truncated = self.mouse.reward(action, self.steps, won)
        obs = self.mouse.observe()

        self.steps += 1

        # # ALWAYS NEEDS TO RETURN: observation, reward, termination, truncation, infos
        return obs, reward, terminated, truncated, {"is_success": won}

    def render(self, mode='rgb_array'):
        """THIS RENDERS PYGAME, DONT RUN DURING TRAINING"""
        if mode == 'human':
            self.screen.fill((0, 0, 0))
            self.mouse.draw(self.screen)
            self.maze.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(20)

        elif mode == 'rgb_array':
            return

    def close(self):
        pygame.quit()
