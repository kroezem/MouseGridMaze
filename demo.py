import pygame
from stable_baselines3 import PPO

from train import latest
from maze_env import MazeEnv


def key_input():
    keys = pygame.key.get_pressed()
    return [
        1 if keys[pygame.K_UP] else 0,
        1 if keys[pygame.K_DOWN] else 0,
        1 if keys[pygame.K_LEFT] else 0,
        1 if keys[pygame.K_RIGHT] else 0
    ]


if __name__ == '__main__':
    env = MazeEnv('./classic', render_mode='human')
    model = PPO.load(latest(), env)

    obs, _ = env.reset()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                exit()

        action, _states = model.predict(obs)
        obs, rewards, terminated, truncated, info = env.step(action)
        env.render('human')

        if terminated or truncated:
            obs, _ = env.reset()

            model_zip = latest()
            print(f'\n******** Loading - {model_zip} ********\n')
            model = PPO.load(model_zip, env)
