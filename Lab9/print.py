import pygame
import sys
import math  # Used for equilateral triangle calculations

pygame.init()

# Set up display dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint Program")

# Define colors (R, G, B)
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
GREEN  = (0,   255, 0)
BLUE   = (0,   0,   255)
YELLOW = (255, 255, 0)

# A palette of selectable colors
color_palette = [BLACK, RED, GREEN, BLUE, YELLOW]
current_color = BLACK  # Default drawing color

background_color = WHITE

# List of available drawing tools (extended with our new shapes)
tools = ["pencil", "rectangle", "circle", "eraser", "square", "right_triangle", "equilateral_triangle", "rhombus"]
current_tool = "pencil"
eraser_radius = 10

# Create a canvas surface to hold drawn content and fill it with the background color
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(background_color)

# Create a preview surface that allows real-time drawing of shapes while dragging
preview = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
preview = preview.convert_alpha()
preview.fill((0, 0, 0, 0))  # Make preview fully transparent

# Drawing state variables
drawing = False      # True when the mouse is held down
start_pos = (0, 0)   # Starting position of the mouse drag
end_pos = (0, 0)     # Current mouse position during drag

clock = pygame.time.Clock()

# ----------------------------- DRAWING FUNCTIONS -----------------------------
def draw_pencil(pos, color):
    """Draw a small circle (simulating a pencil stroke) on the canvas."""
    pygame.draw.circle(canvas, color, pos, 2)

def draw_eraser(pos, radius):
    """Erase by drawing a circle in the background color."""
    pygame.draw.circle(canvas, background_color, pos, radius)

def draw_rectangle(surface, color, start, end):
    """Draw a rectangle defined by the drag start and end positions."""
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    rect = pygame.Rect(min(x1, x2), min(y1, y2), width, height)
    pygame.draw.rect(surface, color, rect, 1)

def draw_circle(surface, color, start, end):
    """Draw a circle based on the distance between start and end positions."""
    x1, y1 = start
    x2, y2 = end
    # Calculate radius as the Euclidean distance between start and end
    radius = int(math.hypot(x2 - x1, y2 - y1))
    pygame.draw.circle(surface, color, start, radius, 1)

def draw_square(surface, color, start, end):
    """
    Draw a square using the starting point as one corner.
    The side length is the minimum of the horizontal and vertical drag distances.
    """
    x1, y1 = start
    x2, y2 = end
    # Determine side length from minimum difference in x and y
    side = min(abs(x2 - x1), abs(y2 - y1))
    # Determine ending coordinates based on the drag direction
    if x2 >= x1:
        x_end = x1 + side
    else:
        x_end = x1 - side
    if y2 >= y1:
        y_end = y1 + side
    else:
        y_end = y1 - side
    rect = pygame.Rect(min(x1, x_end), min(y1, y_end), side, side)
    pygame.draw.rect(surface, color, rect, 1)

def draw_right_triangle(surface, color, start, end):
    """
    Draw a right triangle with the right angle at the start position.
    The triangle's other vertices are determined by projecting the drag end horizontally and vertically from the start.
    """
    x1, y1 = start
    x2, y2 = end
    vertex2 = (x2, y1)  # Horizontal projection from the start
    vertex3 = (x1, y2)  # Vertical projection from the start
    pygame.draw.polygon(surface, color, [start, vertex2, vertex3], 1)

def draw_equilateral_triangle(surface, color, start, end):
    """
    Draw an equilateral triangle using the start and end positions as the base.
    The third vertex is calculated by rotating the base vector by 60 degrees about the start.
    """
    x1, y1 = start
    x2, y2 = end
    # Rotation angle in radians (60 degrees)
    angle = math.radians(60)
    dx = x2 - x1
    dy = y2 - y1
    # Rotate vector (dx, dy) by 60 degrees to calculate the third vertex
    cx = x1 + dx * math.cos(angle) - dy * math.sin(angle)
    cy = y1 + dx * math.sin(angle) + dy * math.cos(angle)
    pygame.draw.polygon(surface, color, [start, end, (cx, cy)], 1)

def draw_rhombus(surface, color, start, end):
    """
    Draw a rhombus (diamond shape) that fits within the rectangle defined by start and end.
    The vertices are the midpoints of the rectangle's sides.
    """
    x1, y1 = start
    x2, y2 = end
    center = ((x1 + x2) / 2, (y1 + y2) / 2)
    left = (min(x1, x2), center[1])
    right = (max(x1, x2), center[1])
    top = (center[0], min(y1, y2))
    bottom = (center[0], max(y1, y2))
    pygame.draw.polygon(surface, color, [top, right, bottom, left], 1)

# ----------------------------- MAIN LOOP -----------------------------
running = True
while running:
    clock.tick(60)  # Limit the frame rate to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check if a color from the palette is selected
            for i, c in enumerate(color_palette):
                palette_rect = pygame.Rect(10 + 50 * i, 10, 40, 40)
                if palette_rect.collidepoint(mouse_x, mouse_y):
                    current_color = c

            # Check if a tool button is selected from the tools list
            for i, t in enumerate(tools):
                tool_rect = pygame.Rect(10 + 50 * i, 60, 40, 40)
                if tool_rect.collidepoint(mouse_x, mouse_y):
                    current_tool = t

            drawing = True
            start_pos = event.pos
            end_pos = event.pos
            # For immediate feedback using pencil or eraser, draw directly
            if current_tool == "pencil":
                draw_pencil(event.pos, current_color)
            elif current_tool == "eraser":
                draw_eraser(event.pos, eraser_radius)

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                # Finalize the shape onto the canvas based on the current tool
                if current_tool == "rectangle":
                    draw_rectangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "circle":
                    draw_circle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "square":
                    draw_square(canvas, current_color, start_pos, end_pos)
                elif current_tool == "right_triangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos)
            # Clear the preview surface after finalizing the shape
            preview.fill((0, 0, 0, 0))

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                end_pos = event.pos
                if current_tool == "pencil":
                    draw_pencil(end_pos, current_color)
                elif current_tool == "eraser":
                    draw_eraser(end_pos, eraser_radius)
                else:
                    # For shapes that use preview, clear and redraw the shape on the preview surface
                    preview.fill((0, 0, 0, 0))
                    if current_tool == "rectangle":
                        draw_rectangle(preview, current_color, start_pos, end_pos)
                    elif current_tool == "circle":
                        draw_circle(preview, current_color, start_pos, end_pos)
                    elif current_tool == "square":
                        draw_square(preview, current_color, start_pos, end_pos)
                    elif current_tool == "right_triangle":
                        draw_right_triangle(preview, current_color, start_pos, end_pos)
                    elif current_tool == "equilateral_triangle":
                        draw_equilateral_triangle(preview, current_color, start_pos, end_pos)
                    elif current_tool == "rhombus":
                        draw_rhombus(preview, current_color, start_pos, end_pos)

    # Blit (copy) the canvas and preview surfaces onto the main screen
    screen.blit(canvas, (0, 0))
    screen.blit(preview, (0, 0))

    # Draw the color palette buttons on the screen
    for i, c in enumerate(color_palette):
        palette_rect = pygame.Rect(10 + 50 * i, 10, 40, 40)
        pygame.draw.rect(screen, c, palette_rect)
        if c == current_color:
            pygame.draw.rect(screen, BLACK, palette_rect, 2)

    # Draw the tool buttons on the screen and label them with the first character
    for i, t in enumerate(tools):
        tool_rect = pygame.Rect(10 + 50 * i, 60, 40, 40)
        pygame.draw.rect(screen, (200, 200, 200), tool_rect)
        font_tool = pygame.font.SysFont(None, 22)
        # For tools with multiple words, you might choose a custom abbreviation. Here we use the first character.
        txt = font_tool.render(t[0].upper(), True, BLACK)
        txt_rect = txt.get_rect(center=tool_rect.center)
        screen.blit(txt, txt_rect)
        if t == current_tool:
            pygame.draw.rect(screen, BLACK, tool_rect, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
