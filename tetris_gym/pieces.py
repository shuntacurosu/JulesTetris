import numpy as np

PIECE_SHAPES = {
    'T': [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (2, 1)]
    ],
    'I': [
        [(1, 0), (1, 1), (1, 2), (1, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)]
    ],
    'O': [
        [(0, 1), (0, 2), (1, 1), (1, 2)]
    ],
    'L': [
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)]
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)]
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 1), (1, 1), (1, 2), (2, 2)]
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 2), (1, 1), (1, 2), (2, 1)]
    ]
}

PIECE_COLORS = {
    'T': 5,  # Magenta
    'I': 6,  # Cyan
    'O': 3,  # Yellow
    'L': 7,  # White
    'J': 4,  # Blue
    'S': 2,  # Green
    'Z': 1   # Red
}

class Piece:
    def __init__(self, shape_name, position=(0, 4)):
        self.name = shape_name
        self.shapes = PIECE_SHAPES[shape_name]
        self.color = PIECE_COLORS[shape_name]
        self.rotation = 0
        self.position = list(position) # [row, col]

    @property
    def shape(self):
        return self.shapes[self.rotation % len(self.shapes)]

    def rotate(self, direction):
        self.rotation = (self.rotation + direction) % len(self.shapes)

    def move(self, dx, dy):
        self.position[0] += dy
        self.position[1] += dx

    def get_coords(self):
        coords = []
        for r_offset, c_offset in self.shape:
            coords.append((self.position[0] + r_offset, self.position[1] + c_offset))
        return coords

class PieceGenerator:
    """Implements the 7-bag random generator."""
    def __init__(self, rng=None):
        self.bag = []
        self.rng = rng if rng is not None else np.random.default_rng()
        self._refill_bag()

    def _refill_bag(self):
        self.bag = list(PIECE_SHAPES.keys())
        self.rng.shuffle(self.bag)

    def next(self):
        if not self.bag:
            self._refill_bag()
        return Piece(self.bag.pop())
