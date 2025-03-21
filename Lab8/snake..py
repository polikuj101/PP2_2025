import pygame
import random
import sys

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 30

# Game-level settings
FOOD_COUNT_FOR_LEVEL_UP = 4
INITIAL_SPEED = 5
LEVEL_SPEED_INCREMENT = 2

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (50, 50, 50)

# --------------------- HELPER FUNCTIONS ---------------------
def draw_snake(surface, snake_body):
    """Draws the snake on the given surface."""
    for segment in snake_body:
        pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def create_random_food(snake_body):
    """
    Returns a (x, y) position for food such that it doesn't overlap
    with the snake's body.
    """
    while True:
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        
        # Make sure food isn't placed on the snake
        if (x, y) not in snake_body:
            return (x, y)

def display_text(surface, text, font, color, x, y):
    """Utility to display text on the given surface."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# --------------------- MAIN GAME FUNCTION ---------------------
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game with Levels")

    clock = pygame.time.Clock()

    # Font for score and level display
    font = pygame.font.SysFont(None, 30)

    # Initial snake setup
    snake_body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # List of (x, y)
    direction = "RIGHT"  # Possible directions: UP, DOWN, LEFT, RIGHT

    # Initial food placement
    food_pos = create_random_food(snake_body)

    # Game stats
    score = 0
    level = 1
    food_eaten_current_level = 0

    # Game speed (cells per tick); movement update is decoupled from the FPS
    snake_speed = INITIAL_SPEED
    move_counter = 0  # Will increment each frame, used to determine when to move snake

    running = True
    while running:
        # --------------------- EVENT HANDLING ---------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        move_counter += 1
        if move_counter >= (FPS // snake_speed):
            move_counter = 0
            head_x, head_y = snake_body[0]

            if direction == "UP":
                head_y -= BLOCK_SIZE
            elif direction == "DOWN":
                head_y += BLOCK_SIZE
            elif direction == "LEFT":
                head_x -= BLOCK_SIZE
            elif direction == "RIGHT":
                head_x += BLOCK_SIZE

            new_head = (head_x, head_y)

            if (head_x < 0 or head_x >= SCREEN_WIDTH or 
                head_y < 0 or head_y >= SCREEN_HEIGHT):
                running = False
            else:
                if new_head in snake_body:
                    running = False
                else:
                    snake_body.insert(0, new_head)

                    if new_head == food_pos:
                        score += 1
                        food_eaten_current_level += 1
                        food_pos = create_random_food(snake_body)

                    if food_eaten_current_level >= FOOD_COUNT_FOR_LEVEL_UP:
                        level += 1
                        food_eaten_current_level = 0
                        snake_speed += LEVEL_SPEED_INCREMENT
                    else:
                        snake_body.pop()      

        screen.fill(BLACK)

        pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        draw_snake(screen, snake_body)

        display_text(screen, f"Score: {score}", font, WHITE, 10, 10)
        display_text(screen, f"Level: {level}", font, WHITE, 10, 40)

        pygame.display.update()
        clock.tick(FPS)

    game_over_screen(screen, font, score, level)
    pygame.quit()
    sys.exit()

def game_over_screen(surface, font, score, level):
    """Displays a simple 'Game Over' screen."""
    surface.fill(BLACK)
    display_text(surface, "GAME OVER", font, RED, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 20)
    display_text(surface, f"Final Score: {score}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 10)
    display_text(surface, f"Level Reached: {level}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 40)
    pygame.display.update()
    pygame.time.delay(2000)  # Wait 2 seconds

if __name__ == "__main__":
    main()
