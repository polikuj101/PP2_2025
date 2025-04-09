import pygame, sys, random, time
from pygame.locals import *

# Initialize pygame modules
pygame.init()

# Setting up Frames Per Second (FPS)
FPS = 60
FramePerSec = pygame.time.Clock()

# Define colors for use
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions and starting game parameters
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5          # Base speed for enemy and coin movement
SCORE = 0          # Number of enemies passed
COINS_COLLECTED = 0  # Total coin "value" collected; coins now have weight

# Threshold for coin weight to boost enemy speed (every 5 coin-units)
COIN_THRESHOLD = 5
# Variable to track how many thresholds have been passed
coin_threshold_count = 0

# Set up fonts for score displays
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("AnimatedStreet.png")

# Set up the display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Define the Enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load enemy image and get its rectangle for positioning
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        # Start enemy at a random horizontal position at the top
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        # Move the enemy down by the current speed
        self.rect.move_ip(0, SPEED)
        # Once the enemy moves beyond the bottom, reposition it at the top
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Define the Player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player image and get its rectangle for positioning
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        # Start player near the bottom center of the screen
        self.rect.center = (160, 520)
       
    def move(self):
        # Check which keys are pressed
        pressed_keys = pygame.key.get_pressed()
        # Move left if left arrow key is pressed and player is not at left screen edge
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        # Move right if right arrow key is pressed and player is not at right screen edge
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Define the Coin sprite class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assign a random coin weight between 1 and 3
        self.weight = random.randint(1, 3)
        # Load the base coin image
        coin_img = pygame.image.load("coin.png")
        # Scale the coin image proportionally to its weight
        # Base size is 25 pixels, and size increases with weight.
        size = 25 * self.weight  
        coin_img = pygame.transform.scale(coin_img, (size, size))
        self.image = coin_img
        self.rect = self.image.get_rect()
        # Set coin starting position at a random horizontal location (taking size into account)
        self.rect.center = (random.randint(size // 2, SCREEN_WIDTH - size // 2), 0)

    def move(self):
        # Move the coin down by the current SPEED
        self.rect.move_ip(0, SPEED)
        # If the coin moves off screen, remove it from all groups
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Create game sprite instances
P1 = Player()
E1 = Enemy()

# Sprite groups for enemies, coins, and all sprites
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Create a custom event that increases speed every second (can be thought of as gradual difficulty increase)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Create a custom event to spawn coins every 2 seconds
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 2000)

# Main game loop
while True:
    for event in pygame.event.get():
        # Gradually increase speed over time as per the event timer
        if event.type == INC_SPEED:
            SPEED += 0.5

        # Spawn a new coin when the SPAWN_COIN event is triggered
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        # Handle quitting the game window
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw the background image
    DISPLAYSURF.blit(background, (0, 0))

    # Display the number of enemies passed (score) at top-left
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Display the total collected coin weight at top-right
    coins_text = font_small.render(str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 30, 10))

    # Move and draw all sprites (player, enemy, coins)
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check collision between the player and any enemy sprite
    if pygame.sprite.spritecollideany(P1, enemies):
        # Play crash sound, show game over screen and end game
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()  

    # Check collision between the player and coins.
    # The coins that collide are removed from the game.
    coin_collisions = pygame.sprite.spritecollide(P1, coins, True)
    if coin_collisions:
        # Add the weight (value) of each collected coin to the total coin collection
        for coin in coin_collisions:
            COINS_COLLECTED += coin.weight

        # Increase enemy speed when a coin threshold is met.
        # Use integer division to count how many thresholds have been reached.
        new_threshold_count = COINS_COLLECTED // COIN_THRESHOLD
        if new_threshold_count > coin_threshold_count:
            # Increase enemy (and coin) speed by 1 unit for each new threshold passed.
            SPEED += 1
            coin_threshold_count = new_threshold_count

    # Update the display and maintain the set FPS
    pygame.display.update()
    FramePerSec.tick(FPS)
