import pytest
import numpy as np

from tetris_gym.board import Board
from tetris_gym.pieces import Piece, PIECE_COLORS

@pytest.fixture
def board():
    """Pytest fixture to provide a clean board instance for each test function."""
    return Board(width=10, height=20)

def test_initialization(board):
    """Test that the board initializes correctly."""
    assert board.width == 10
    assert board.height == 20
    assert board.score == 0
    assert not board.game_over
    assert board.current_piece is not None
    assert np.all(board.grid == 0)

def test_piece_move_valid(board):
    """Test that a piece can move within bounds."""
    initial_pos = board.current_piece.position.copy()
    # Move right
    can_move = board.move(1, 0)
    assert can_move
    assert board.current_piece.position[1] == initial_pos[1] + 1
    # Move left
    can_move = board.move(-1, 0)
    assert can_move
    assert board.current_piece.position == initial_pos

def test_piece_move_invalid_wall(board):
    """Test that a piece cannot move outside the walls."""
    # Move piece all the way to the left edge
    for _ in range(5):
        board.move(-1, 0)

    initial_pos = board.current_piece.position.copy()
    # Attempt to move further left
    can_move = board.move(-1, 0)
    assert not can_move
    assert board.current_piece.position == initial_pos

def test_line_clear(board):
    """Test that a full line is cleared correctly."""
    # Manually create a full line on the bottom row
    board.grid[19, 1:] = 1  # Fill all but the first column

    # Create an 'I' piece and position it to fill the gap
    # The 'I' piece is a horizontal line at its default rotation
    i_piece = Piece('I')
    i_piece.rotation = 1 # Make it a vertical line
    # Position the piece so its falling path aligns with the gap at column 0
    i_piece.position = [16, -2]
    board.current_piece = i_piece

    # Hard drop the piece to fill the line and trigger clear
    board.hard_drop()

    assert board.lines_cleared == 1

    # The bottom row should now be the row that was above the cleared line.
    # In this test, row 18, which was empty except for the I-piece block.
    expected_bottom_row = np.zeros(10, dtype=int)
    expected_bottom_row[0] = PIECE_COLORS['I']

    assert np.array_equal(board.grid[19], expected_bottom_row)
    assert board.score > 0

def test_game_over(board):
    """Test the game over condition."""
    # Fill the top of the board so a new piece causes a collision immediately
    board.grid[0:2, :] = 1
    board._spawn_piece()
    assert board.game_over
