import pygame
import os
import sys

pygame.init()

WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

music_folder = "C:/Users/nurbolatte/Music"
songs = [f for f in os.listdir(music_folder) if f.endswith(".wav")]
current_song_index = 0

pygame.mixer.init()


def load_song(index):
    pygame.mixer.music.load(os.path.join(music_folder, songs[index]))
    pygame.mixer.music.play()


if songs:
    load_song(current_song_index)


font = pygame.font.Font(None, 30)


def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + 10, y + 10))


def draw_text(text, x, y):
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))


running = True
while running:
    screen.fill(WHITE)

    if songs:
        song_name = f"Now Playing: {songs[current_song_index]}"
    else:
        song_name = "No songs available"
    
    draw_text(song_name, 20, 20)

    draw_button("Play", 50, 80, 80, 40)
    draw_button("Stop", 150, 80, 80, 40)
    draw_button("Next", 250, 80, 80, 40)
    draw_button("Prev", 50, 140, 80, 40)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:
                current_song_index = (current_song_index + 1) % len(songs)
                load_song(current_song_index)
            elif event.key == pygame.K_p:
                pygame.mixer.music.play()
                load_song(current_song_index)

pygame.quit()
sys.exit()
