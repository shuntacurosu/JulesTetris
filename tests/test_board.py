import unittest
import numpy as np

from tetris_gym.board import Board
from tetris_gym.pieces import Piece

class TestBoard(unittest.TestCase):

    def setUp(self):
        """Set up a new board for each test."""
        self.board = Board(width=10, height=20)

    def test_initialization(self):
        """Test that the board initializes correctly."""
        self.assertEqual(self.board.width, 10)
        self.assertEqual(self.board.height, 20)
        self.assertEqual(self.board.score, 0)
        self.assertFalse(self.board.game_over)
        self.assertIsNotNone(self.board.current_piece)
        self.assertTrue(np.all(self.board.grid == 0))

    def test_piece_move_valid(self):
        """Test that a piece can move within bounds."""
        initial_pos = self.board.current_piece.position.copy()
        # Move right
        can_move = self.board.move(1, 0)
        self.assertTrue(can_move)
        self.assertEqual(self.board.current_piece.position[1], initial_pos[1] + 1)
        # Move left
        can_move = self.board.move(-1, 0)
        self.assertTrue(can_move)
        self.assertEqual(self.board.current_piece.position, initial_pos)

    def test_piece_move_invalid_wall(self):
        """Test that a piece cannot move outside the walls."""
        # Move piece all the way to the left edge
        for _ in range(5):
            self.board.move(-1, 0)

        initial_pos = self.board.current_piece.position.copy()
        # Attempt to move further left
        can_move = self.board.move(-1, 0)
        self.assertFalse(can_move)
        self.assertEqual(self.board.current_piece.position, initial_pos)

    def test_line_clear(self):
        """Test that a full line is cleared correctly."""
        # Manually create a full line, leaving one column empty for the last piece
        self.board.grid[19, 1:] = 1

        # Create a piece that will fill the gap (e.g., an 'I' piece)
        i_piece = Piece('I')
        i_piece.position = [18, 0] # Position it to fall into the gap
        self.board.current_piece = i_piece

        # Drop the piece to fill the line
        self.board.drop() # This should lock the piece and clear the line

        self.assertEqual(self.board.lines_cleared, 1)
        self.assertTrue(np.all(self.board.grid[19] == 0)) # Bottom line should be cleared
        self.assertGreater(self.board.score, 0)

    def test_game_over(self):
        """Test the game over condition."""
        # Fill the top of the board so a new piece causes a collision immediately
        self.board.grid[0:2, :] = 1
        self.board._spawn_piece()
        self.assertTrue(self.board.game_over)

if __name__ == '__main__':
    unittest.main()
