# ===============================
# File: food.py
# ===============================
import random
from constants import GRID_WIDTH, GRID_HEIGHT

class Food:
    """Represents the food item that the snake eats."""
    
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
    
    def spawn(self, snake_body=None):
        """Place food at a random empty cell (avoid snake body)."""
        if snake_body is None:
            snake_body = []
        
        # Convert snake body to set for faster lookup
        occupied = set(snake_body)
        
        # Generate random positions until we find an empty one
        # (in worst case, could loop forever, but grid is large enough)
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in occupied:
                self.position = (x, y)
                break
    
    def get_position(self):
        """Return current food position."""
        return self.position
