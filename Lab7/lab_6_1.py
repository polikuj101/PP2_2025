import pygame
import sys
from datetime import datetime

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()

mickey_face = pygame.image.load("clock.png").convert_alpha()
minute_hand_img = pygame.image.load("rightarm.png").convert_alpha()
second_hand_img = pygame.image.load("leftarm.png").convert_alpha()
def blit_rotate(surf, image, pivot, pivot_offset, angle):
   
    image_rect = image.get_rect(topleft=(pivot[0] - pivot_offset[0],
                                         pivot[1] - pivot_offset[1]))
    
    rotated_image = pygame.transform.rotate(image, -angle)
    
    rotated_rect = rotated_image.get_rect(center=image_rect.center)
    
    surf.blit(rotated_image, rotated_rect)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.now()
    minutes = now.minute
    seconds = now.second

    minute_angle = minutes * 6
    second_angle = seconds * 6

    screen.fill((255, 255, 255))

    face_rect = mickey_face.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(mickey_face, face_rect)
    pivot_x = WIDTH // 2
    pivot_y = HEIGHT // 2

    minute_offset = (700, 525)  
    second_offset = (25, 525)  

    blit_rotate(screen, second_hand_img,
                pivot=(pivot_x, pivot_y),
                pivot_offset=second_offset,
                angle=second_angle)

    blit_rotate(screen, minute_hand_img,
                pivot=(pivot_x, pivot_y),
                pivot_offset=minute_offset,
                angle=minute_angle)

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
sys.exit()
