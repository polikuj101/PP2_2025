import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((640, 640))


RADIUS = 25
x = 640 // 2
y = 640 // 2

SPEED = 5

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        y -= SPEED
    if keys[pygame.K_DOWN]:
        y += SPEED
    if keys[pygame.K_LEFT]:
        x -= SPEED
    if keys[pygame.K_RIGHT]:
        x += SPEED

    x = max(RADIUS, min(640 - RADIUS, x))
    y = max(RADIUS, min(640 - RADIUS, y))

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), (x, y), RADIUS)

    pygame.display.flip()

pygame.quit()
sys.exit()
