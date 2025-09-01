from gymnasium.envs.registration import register

# Register the Tetris environment
register(
    id='TetrisEnv-v0',
    entry_point='tetris_gym.env:TetrisEnv',
    max_episode_steps=10000,
)

# Make TetrisEnv available when importing tetris_gym
from tetris_gym.env import TetrisEnv

__all__ = ['TetrisEnv']