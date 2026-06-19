# ===============================
# File: snake.py
# ===============================
import random
from constants import (
    GRID_WIDTH, GRID_HEIGHT, INITIAL_SNAKE, INITIAL_DIRECTION,
    UP, DOWN, LEFT, RIGHT
)

class Snake:
    """Represents the snake, its movement, growth, and collision detection."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset snake to starting state."""
        self.body = list(INITIAL_SNAKE)          # list of (x, y) tuples
        self.direction = INITIAL_DIRECTION
        self.next_direction = INITIAL_DIRECTION
        self.grow_flag = False
    
    def set_direction(self, direction):
        """Set the next movement direction (cannot reverse)."""
        # Prevent reversing into itself
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def move(self):
        """Move the snake one step forward."""
        # Apply the queued direction
        self.direction = self.next_direction
        
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Insert new head
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        """Set flag to grow on next move."""
        self.grow_flag = True
    
    def check_self_collision(self):
        """Return True if head collides with its body (excluding head)."""
        head = self.body[0]
        return head in self.body[1:]
    
    def check_wall_collision(self):
        """Return True if head is outside grid boundaries."""
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= GRID_WIDTH or
                head_y < 0 or head_y >= GRID_HEIGHT)
    
    def check_food_collision(self, food_pos):
        """Return True if head is at the food position."""
        return self.body[0] == food_pos
    
    def get_head(self):
        """Return head position."""
        return self.body[0]
    
    def get_body(self):
        """Return full body list."""
        return self.body
