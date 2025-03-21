import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint Program")

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (255, 0,   0)
GREEN = (0,   255, 0)
BLUE  = (0,   0,   255)
YELLOW= (255, 255, 0)

# A small palette of colors to choose from
color_palette = [BLACK, RED, GREEN, BLUE, YELLOW]
current_color = BLACK  # Default drawing color

background_color = WHITE

tools = ["pencil", "rectangle", "circle", "eraser"]
current_tool = "pencil"
eraser_radius = 10

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(background_color)

# For real-time drawing of shapes while dragging
preview = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
preview = preview.convert_alpha()
preview.fill((0, 0, 0, 0))  # Transparent

# -----------------------------
drawing = False      # True when the mouse is held down
start_pos = (0, 0)   # Where the drag started (for shapes)
end_pos = (0, 0)     # Current mouse position (for shapes)

clock = pygame.time.Clock()

def draw_pencil(pos, color):
    """Draw a small line or point (like a pencil) on the canvas."""
    pygame.draw.circle(canvas, color, pos, 2)

def draw_eraser(pos, radius):
    """Erase by drawing a circle in the background color."""
    pygame.draw.circle(canvas, background_color, pos, radius)

def draw_rectangle(surface, color, start, end):
    """Draw a rectangle from start to end on the given surface."""
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    rect = pygame.Rect(min(x1,x2), min(y1,y2), width, height)
    pygame.draw.rect(surface, color, rect, 1)

def draw_circle(surface, color, start, end):
    """Draw a circle on the given surface based on start-end drag."""
    x1, y1 = start
    x2, y2 = end
    radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, 1)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            for i, c in enumerate(color_palette):
                palette_rect = pygame.Rect(10 + 50 * i, 10, 40, 40)
                if palette_rect.collidepoint(mouse_x, mouse_y):
                    current_color = c

            for i, t in enumerate(tools):
                tool_rect = pygame.Rect(10 + 50*i, 60, 40, 40)
                if tool_rect.collidepoint(mouse_x, mouse_y):
                    current_tool = t

            drawing = True
            start_pos = event.pos
            end_pos = event.pos
            if current_tool == "pencil":
                draw_pencil(event.pos, current_color)
            elif current_tool == "eraser":
                draw_eraser(event.pos, eraser_radius)

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                # Finalize shape onto the canvas
                if current_tool == "rectangle":
                    draw_rectangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "circle":
                    draw_circle(canvas, current_color, start_pos, end_pos)
            # Clear preview after finalizing
            preview.fill((0, 0, 0, 0))

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                end_pos = event.pos
                if current_tool == "pencil":
                    draw_pencil(end_pos, current_color)
                elif current_tool == "eraser":
                    draw_eraser(end_pos, eraser_radius)
                else:
                    # Rectangle or Circle: draw on preview
                    preview.fill((0, 0, 0, 0))
                    if current_tool == "rectangle":
                        draw_rectangle(preview, current_color, start_pos, end_pos)
                    elif current_tool == "circle":
                        draw_circle(preview, current_color, start_pos, end_pos)

    screen.blit(canvas, (0, 0))
    screen.blit(preview, (0, 0))

    for i, c in enumerate(color_palette):
        palette_rect = pygame.Rect(10 + 50*i, 10, 40, 40)
        pygame.draw.rect(screen, c, palette_rect)
        if c == current_color:
            pygame.draw.rect(screen, BLACK, palette_rect, 2)

    for i, t in enumerate(tools):
        tool_rect = pygame.Rect(10 + 50*i, 60, 40, 40)
        pygame.draw.rect(screen, (200, 200, 200), tool_rect)
        font = pygame.font.SysFont(None, 22)
        txt = font.render(t[0].upper(), True, BLACK)
        txt_rect = txt.get_rect(center=tool_rect.center)
        screen.blit(txt, txt_rect)

        if t == current_tool:
            pygame.draw.rect(screen, BLACK, tool_rect, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
