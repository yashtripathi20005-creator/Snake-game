# ===============================
# File: game.py
# ===============================
import pygame
import sys
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    BLACK, WHITE, GREEN, RED, DARK_GREEN, GRAY, SCORE_BG, TEXT_COLOR,
    SPEED_NORMAL
)
from snake import Snake
from food import Food

class Game:
    """Main game controller: manages state, rendering, and event loop."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        
        self.reset()
    
    def reset(self):
        """Reset the game to initial state."""
        self.snake = Snake()
        self.food = Food()
        # Ensure food doesn't spawn on snake
        self.food.spawn(self.snake.get_body())
        self.score = 0
        self.game_over = False
        self.paused = False
        self.move_timer = 0
        self.speed = SPEED_NORMAL
    
    def handle_events(self):
        """Process keyboard and quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset()
                    continue
                
                # Pause toggle
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    continue
                
                # Direction controls (only if not paused)
                if not self.paused:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.set_direction((0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.set_direction((0, 1))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.set_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.set_direction((1, 0))
    
    def update(self):
        """Update game logic (movement, collisions, scoring)."""
        if self.game_over or self.paused:
            return
        
        # Move snake at fixed intervals
        self.move_timer += self.clock.get_time()
        if self.move_timer >= self.speed:
            self.move_timer = 0
            
            # Move the snake
            self.snake.move()
            
            # Check wall collision
            if self.snake.check_wall_collision():
                self.game_over = True
                return
            
            # Check self collision
            if self.snake.check_self_collision():
                self.game_over = True
                return
            
            # Check food collision
            if self.snake.check_food_collision(self.food.get_position()):
                self.snake.grow()
                self.score += 1
                self.food.spawn(self.snake.get_body())
    
    def draw(self):
        """Render everything on screen."""
        self.screen.fill(BLACK)
        
        # Draw grid lines (subtle)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw food
        fx, fy = self.food.get_position()
        food_rect = pygame.Rect(fx * GRID_SIZE, fy * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, RED, food_rect)
        # Inner highlight for food
        inner_rect = pygame.Rect(fx * GRID_SIZE + 3, fy * GRID_SIZE + 3, GRID_SIZE - 6, GRID_SIZE - 6)
        pygame.draw.rect(self.screen, (255, 120, 120), inner_rect)
        
        # Draw snake
        for idx, (sx, sy) in enumerate(self.snake.get_body()):
            rect = pygame.Rect(sx * GRID_SIZE, sy * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if idx == 0:
                # Head: brighter green
                pygame.draw.rect(self.screen, (0, 255, 0), rect)
                pygame.draw.rect(self.screen, (100, 255, 100), rect, 2)
            else:
                # Body: gradient from dark green to green
                intensity = max(30, 180 - (idx * 3))
                color = (0, intensity, 0)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, DARK_GREEN, rect, 1)
        
        # Draw score (top-left with background)
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        score_bg = pygame.Rect(5, 5, score_text.get_width() + 20, score_text.get_height() + 10)
        pygame.draw.rect(self.screen, SCORE_BG, score_bg, border_radius=8)
        self.screen.blit(score_text, (15, 10))
        
        # Draw pause indicator
        if self.paused:
            pause_surf = self.big_font.render("PAUSED", True, WHITE)
            pause_rect = pause_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(pause_surf, pause_rect)
            sub = self.font.render("Press P to resume", True, TEXT_COLOR)
            sub_rect = sub.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(sub, sub_rect)
        
        # Draw game over overlay
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            go_text = self.big_font.render("GAME OVER", True, RED)
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(go_text, go_rect)
            
            score_text2 = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect2 = score_text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(score_text2, score_rect2)
            
            restart_text = self.font.render("Press R to restart", True, TEXT_COLOR)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)   # Limit to 60 FPS
