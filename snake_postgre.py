import pygame
import random
import sys

# Import our DB helper methods
from task2 import (
    create_tables,
    get_or_create_user,
    get_latest_user_score,
    save_user_score
)

# 1) Ensure the tables exist
create_tables()

# 2) Prompt the user for their username
username_input = input("Enter your username: ")
user_id = get_or_create_user(username_input)

# 3) Fetch the latest (level, score)
start_level, start_score = get_latest_user_score(user_id)
print(f"Welcome, {username_input}! You are starting at level {start_level} with score {start_score}.")

# 4) Pygame setup
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - PostgreSQL Edition")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (128, 128, 128)
FOOD_COLOR = (255, 165, 0)

# Level configurations: Each level can define a speed and walls
level_configs = {
    1: (5, []),
    2: (7, [(100,100, 400,20), (100, 100, 20, 400)]),
    3: (9, [(200,200, 200,20), (200, 300, 20, 200)])
}
DEFAULT_SPEED = 10

# Game variables
snake_body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
direction = "RIGHT"
score = start_score
level = start_level

if level in level_configs:
    snake_speed, walls = level_configs[level]
else:
    snake_speed, walls = DEFAULT_SPEED, []

paused = False

# Food creation
def create_random_food(snake_body):
    while True:
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        if (x, y) not in snake_body:
            return (x, y)

food_pos = create_random_food(snake_body)
move_counter = 0

# Helper functions
def draw_snake(surface, snake_body):
    for segment in snake_body:
        pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_walls(surface, wall_list):
    for wall in wall_list:
        pygame.draw.rect(surface, GRAY, wall)

def check_wall_collision(head, wall_list):
    head_rect = pygame.Rect(head[0], head[1], BLOCK_SIZE, BLOCK_SIZE)
    for wall in wall_list:
        wall_rect = pygame.Rect(wall)
        if head_rect.colliderect(wall_rect):
            return True
    return False

def display_text(surface, text, x, y, color=WHITE):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, rect)

# Main loop
running = True
while running:
    clock.tick(FPS)

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

            # Press 'P' to pause/unpause
            elif event.key == pygame.K_p:
                paused = not paused
                if paused:
                    # Save current state to DB
                    save_user_score(user_id, level, score)

    if paused:
        # Display "paused"
        screen.fill(BLACK)
        display_text(screen, "PAUSED (press 'P' to resume)", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, RED)
        pygame.display.update()
        continue

    # Move snake at a rate dependent on snake_speed
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

        # Check collisions with edges
        if (head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT):
            running = False
        else:
            # Check collisions with self
            if new_head in snake_body:
                running = False
            # Check collisions with walls
            elif check_wall_collision(new_head, walls):
                running = False
            else:
                snake_body.insert(0, new_head)
                # Check food
                if new_head == food_pos:
                    score += 1
                    food_pos = create_random_food(snake_body)
                    # Level up logic (e.g., every 5 points)
                    if score % 5 == 0:
                        level += 1
                        if level in level_configs:
                            snake_speed, walls = level_configs[level]
                        else:
                            snake_speed, walls = DEFAULT_SPEED, []
                else:
                    snake_body.pop()

    # Draw
    screen.fill(BLACK)
    draw_walls(screen, walls)
    pygame.draw.rect(screen, FOOD_COLOR, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
    draw_snake(screen, snake_body)

    display_text(screen, f"User: {username_input}", 10, 10)
    display_text(screen, f"Level: {level}", 10, 40)
    display_text(screen, f"Score: {score}", 10, 70)
    display_text(screen, "[P] Pause/Save", SCREEN_WIDTH - 140, 10)

    pygame.display.update()

# Game Over
# Save final state so next time user resumes from this level/score
save_user_score(user_id, level, score)

screen.fill(BLACK)
display_text(screen, "GAME OVER!", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 20, RED)
display_text(screen, f"Final Score: {score}", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 20)
pygame.display.update()
pygame.time.wait(2000)

pygame.quit()
sys.exit()
