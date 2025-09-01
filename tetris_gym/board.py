import numpy as np
from tetris_gym.pieces import PieceGenerator

class Board:
    def __init__(self, width=10, height=20, rng=None):
        self.width = width
        self.height = height
        self.rng = rng if rng is not None else np.random.default_rng()
        self.piece_generator = PieceGenerator(rng=self.rng)
        self.reset(rng=self.rng)

    def reset(self, rng=None):
        """Resets the game board to its initial state."""
        if rng is not None:
            self.rng = rng

        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.piece_generator = PieceGenerator(rng=self.rng)
        self.current_piece = None
        self._spawn_piece()

    def _spawn_piece(self):
        """Spawns a new piece at the top of the board."""
        self.current_piece = self.piece_generator.next()
        # Check for game over condition
        if self._is_collision(self.current_piece.get_coords()):
            self.game_over = True

    def _is_collision(self, coords):
        """Checks if the given coordinates collide with the board boundaries or existing pieces."""
        for r, c in coords:
            if not (0 <= c < self.width and 0 <= r < self.height):
                return True  # Wall collision
            if r >= 0 and self.grid[r, c] > 0:
                return True  # Piece collision
        return False

    def move(self, dx, dy):
        """Moves the current piece. Returns True if successful, False otherwise."""
        self.current_piece.move(dx, dy)
        if self._is_collision(self.current_piece.get_coords()):
            self.current_piece.move(-dx, -dy) # Revert move
            return False
        return True

    def rotate(self, direction):
        """Rotates the current piece. Returns True if successful, False otherwise."""
        original_rotation = self.current_piece.rotation
        self.current_piece.rotate(direction)
        if self._is_collision(self.current_piece.get_coords()):
            self.current_piece.rotation = original_rotation # Revert rotation
            return False
        return True

    def _lock_piece(self):
        """Locks the current piece onto the grid."""
        for r, c in self.current_piece.get_coords():
            if r >= 0:
                self.grid[r, c] = self.current_piece.color
        self._clear_lines()
        self._spawn_piece()

    def _clear_lines(self):
        """Clears completed lines and updates score."""
        lines_to_clear = [r for r in range(self.height) if np.all(self.grid[r] > 0)]
        num_cleared = len(lines_to_clear)

        if num_cleared > 0:
            # Simple scoring: 100 per line, with a bonus for multiple lines
            self.score += 100 * num_cleared * num_cleared
            self.lines_cleared += num_cleared
            # Remove the cleared lines
            for r in lines_to_clear:
                self.grid[r] = 0 # Clear the line
            # Shift lines down
            cleared_grid = np.delete(self.grid, lines_to_clear, axis=0)
            new_lines = np.zeros((num_cleared, self.width), dtype=int)
            self.grid = np.vstack((new_lines, cleared_grid))

    def drop(self):
        """Drops the piece one line. If it collides, lock it."""
        if not self.move(0, 1):
            self._lock_piece()
            self.score += 1 # Reward for placing a piece
            return False
        return True

    def hard_drop(self):
        """Drops the piece to the bottom instantly."""
        while self.move(0, 1):
            pass
        self._lock_piece()
        self.score += 2 # Slightly higher reward for hard drop
