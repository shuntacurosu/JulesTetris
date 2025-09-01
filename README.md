# Tetris Gym Environment

This project is a Tetris game environment compliant with Gymnasium (formerly Gym), designed for future reinforcement learning research.
This initial version implements manual play by a human.

## Features

- Gymnasium `Env` compatible interface (`step`, `reset`, `render`, `close`)
- CUI-based gameplay
- Standard Tetris rules

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## How to Play

Run the following command:

```bash
python play.py
```

Controls:
- **A/D or ←/→**: Move left/right
- **S or ↓**: Soft drop
- **W or ↑**: Rotate
- **Space**: Hard drop
- **Q**: Quit game
