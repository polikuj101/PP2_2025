import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and block size for snake segments and food blocks
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 30

# Game-level settings
FOOD_COUNT_FOR_LEVEL_UP = 4       # Number of foods eaten to level up
INITIAL_SPEED = 5                 # Initial snake speed (affects movement frequency)
LEVEL_SPEED_INCREMENT = 2         # Increment of snake speed at each level up
FOOD_LIFETIME = 5000              # Food lifetime in milliseconds (e.g., 5000ms = 5 seconds)

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
    Generates a (x, y) position for food such that it does not overlap with the snake's body.
    Returns:
        tuple: (x, y) food position.
    """
    while True:
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        # Ensure the food is not placed on the snake
        if (x, y) not in snake_body:
            return (x, y)

def display_text(surface, text, font, color, x, y):
    """Utility function to render and display text on the given surface."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# --------------------- FOOD CLASS ---------------------
class Food:
    def __init__(self, snake_body):
        """
        Initializes a new food item with random weight and a position
        that does not conflict with the snake. Records its spawn time.
        """
        self.weight = random.randint(1, 3)  # Assign a random weight between 1 and 3
        self.position = create_random_food(snake_body)  # Generate random position
        self.spawn_time = pygame.time.get_ticks()  # Record the creation time of the food

    def draw(self, surface, font):
        """
        Draws the food as a red block on the surface, with its weight displayed in the center.
        """
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))
        # Render the weight value on the food block for visual feedback
        weight_text = font.render(str(self.weight), True, BLACK)
        text_rect = weight_text.get_rect(center=(self.position[0] + BLOCK_SIZE/2, self.position[1] + BLOCK_SIZE/2))
        surface.blit(weight_text, text_rect)

# --------------------- MAIN GAME FUNCTION ---------------------
def main():
    # Set up the game window and caption
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game with Weighted Food and Timers")

    clock = pygame.time.Clock()

    # Font for score, level, and food weight display
    font = pygame.font.SysFont(None, 30)

    # Initial snake setup: start in the center of the screen
    snake_body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # List to track snake segments (x, y)
    direction = "RIGHT"  # Initial direction (can be UP, DOWN, LEFT, or RIGHT)

    # Create the first food object
    current_food = Food(snake_body)

    # Initialize game stats
    score = 0
    level = 1
    food_eaten_current_level = 0
    snake_speed = INITIAL_SPEED  # Speed factor determining the snake's movement frequency
    move_counter = 0             # Counter to regulate movement based on snake_speed

    running = True
    while running:
        # --------------------- EVENT HANDLING ---------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Update snake direction while preventing opposite direction moves
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # --------------------- SNAKE MOVEMENT ---------------------
        move_counter += 1
        # Move the snake when the move counter reaches the threshold based on speed
        if move_counter >= (FPS // snake_speed):
            move_counter = 0
            head_x, head_y = snake_body[0]

            # Update the head coordinates based on current direction
            if direction == "UP":
                head_y -= BLOCK_SIZE
            elif direction == "DOWN":
                head_y += BLOCK_SIZE
            elif direction == "LEFT":
                head_x -= BLOCK_SIZE
            elif direction == "RIGHT":
                head_x += BLOCK_SIZE

            new_head = (head_x, head_y)

            # Check if the new head is outside the boundaries or it collides with the snake body
            if (head_x < 0 or head_x >= SCREEN_WIDTH or 
                head_y < 0 or head_y >= SCREEN_HEIGHT or 
                new_head in snake_body):
                running = False
            else:
                snake_body.insert(0, new_head)  # Add new head position to snake body

                # --------------------- FOOD COLLISION CHECK ---------------------
                if new_head == current_food.position:
                    # Increase score by the weight of the food eaten
                    score += current_food.weight
                    food_eaten_current_level += 1

                    # Generate a new food item after eating the current one
                    current_food = Food(snake_body)
                else:
                    # If no food eaten, remove the tail segment to simulate movement
                    snake_body.pop()

            # --------------------- LEVEL UP LOGIC ---------------------
            if food_eaten_current_level >= FOOD_COUNT_FOR_LEVEL_UP:
                level += 1
                food_eaten_current_level = 0
                snake_speed += LEVEL_SPEED_INCREMENT

        # --------------------- FOOD TIMER CHECK ---------------------
        # If the food has been on screen longer than its lifetime, generate a new food item
        if pygame.time.get_ticks() - current_food.spawn_time > FOOD_LIFETIME:
            current_food = Food(snake_body)

        # --------------------- DRAWING ---------------------
        screen.fill(BLACK)  # Clear screen with black
        # Draw current food
        current_food.draw(screen, font)
        # Draw snake
        draw_snake(screen, snake_body)
        # Display the current score and level
        display_text(screen, f"Score: {score}", font, WHITE, 10, 10)
        display_text(screen, f"Level: {level}", font, WHITE, 10, 40)

        pygame.display.update()
        clock.tick(FPS)

    game_over_screen(screen, font, score, level)
    pygame.quit()
    sys.exit()

def game_over_screen(surface, font, score, level):
    """
    Displays a simple game over screen with final score and level reached.
    """
    surface.fill(BLACK)
    display_text(surface, "GAME OVER", font, RED, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 20)
    display_text(surface, f"Final Score: {score}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 10)
    display_text(surface, f"Level Reached: {level}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 40)
    pygame.display.update()
    pygame.time.delay(2000)  # Pause for 2 seconds to allow the player to see the final stats

if __name__ == "__main__":
    main()
