# ===============================
# File: constants.py
# ===============================
# Game configuration constants

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Grid settings (classic 20x20 grid)
GRID_SIZE = 20          # pixels per cell
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE   # 30 cells
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE # 30 cells

# Speeds (update intervals in milliseconds)
SPEED_SLOW = 150
SPEED_NORMAL = 100
SPEED_FAST = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
DARK_GREEN = (0, 180, 0)
GRAY = (40, 40, 40)
SCORE_BG = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initial snake
INITIAL_SNAKE = [(5, 15), (4, 15), (3, 15)]
INITIAL_DIRECTION = RIGHT
