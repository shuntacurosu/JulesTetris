import gymnasium as gym
from gymnasium import spaces
import numpy as np
import os

from tetris_gym.board import Board

class TetrisEnv(gym.Env):
    """A Tetris environment for Gymnasium."""
    metadata = {'render_modes': ['human', 'ansi'], 'render_fps': 30}

    def __init__(self, render_mode='human'):
        super().__init__()
        self.board = Board() # Created once
        self.render_mode = render_mode

        # Action space: 0:No-op, 1:Left, 2:Right, 3:SoftDrop, 4:Rot-CW, 5:Rot-CCW, 6:HardDrop
        self.action_space = spaces.Discrete(7)

        # Observation space: game board, next piece
        # The number of pieces is fixed (7 types)
        self.observation_space = spaces.Dict({
            "board": spaces.Box(0, 7, shape=(self.board.height, self.board.width), dtype=np.uint8),
            "next_piece": spaces.Discrete(7)
        })

    def _get_obs(self):
        # Create a copy of the board grid to draw the current piece on it
        grid_with_piece = self.board.grid.copy()
        if self.board.current_piece:
            for r, c in self.board.current_piece.get_coords():
                if 0 <= r < self.board.height and 0 <= c < self.board.width:
                    grid_with_piece[r, c] = self.board.current_piece.color

        # Get next piece's index
        # The next piece is the last one in the current bag.
        # If the bag is empty, the generator will refill it on the next call,
        # so we can peek at the bag that will be used for the *next* piece.
        if not self.board.piece_generator.bag:
            self.board.piece_generator._refill_bag() # Ensure bag is not empty for observation

        next_piece_name = self.board.piece_generator.bag[-1]

        # A simple mapping to int for the observation space
        piece_map = {name: i for i, name in enumerate(list('TIOLJSZ'))}
        next_piece_idx = piece_map.get(next_piece_name, 0)

        return {"board": grid_with_piece.astype(np.uint8), "next_piece": next_piece_idx}

    def _get_info(self):
        return {
            "score": self.board.score,
            "lines_cleared": self.board.lines_cleared,
            "game_over": self.board.game_over
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Pass the seeded random number generator to the board's reset method
        self.board.reset(rng=self.np_random)
        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def step(self, action):
        prev_score = self.board.score

        if action == 0: # No-op (let piece fall)
            self.board.drop()
        elif action == 1: # Move Left
            self.board.move(-1, 0)
        elif action == 2: # Move Right
            self.board.move(1, 0)
        elif action == 3: # Soft Drop
            self.board.drop()
        elif action == 4: # Rotate Clockwise
            self.board.rotate(1)
        elif action == 5: # Rotate Counter-Clockwise
            self.board.rotate(-1)
        elif action == 6: # Hard Drop
            self.board.hard_drop()

        terminated = self.board.game_over
        reward = self.board.score - prev_score
        if terminated:
            reward -= 100 # Penalty for game over

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == 'human':
            self.render()

        # `truncated` is for time limits, which we don't have.
        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == 'ansi':
            return self._render_to_ansi()

        # 'human' render mode
        grid = self._get_obs()['board']
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Tetris Gym")
        print("=" * (self.board.width * 2 + 2))
        for row in grid:
            print("|" + "".join([("██" if cell > 0 else "  ") for cell in row]) + "|")
        print("=" * (self.board.width * 2 + 2))
        print(f"Score: {self.board.score} | Lines: {self.board.lines_cleared}")

        # Print next piece (simple version)
        if self.board.piece_generator.bag:
            next_piece_name = self.board.piece_generator.bag[-1]
            print(f"Next Piece: {next_piece_name}")

    def _render_to_ansi(self):
        # For non-human rendering, return a string representation
        grid = self._get_obs()['board']
        ansi_str = ""
        for row in grid:
            ansi_str += "".join([("█" if cell > 0 else " ") for cell in row]) + "\n"
        return ansi_str

    def close(self):
        pass
