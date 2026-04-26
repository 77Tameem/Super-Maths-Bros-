import pygame


# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Track Outline')

# Load the track image
track_image = pygame.image.load('graphics/track.png')

# Create a mask from the track image
track_mask = pygame.mask.from_surface(track_image)

# Function to draw the outline of the mask
def draw_outline(screen, mask, offset=(0, 0), color=(255, 0, 0), width=2):
    outline = mask.outline()
    outline = [(point[0] + offset[0], point[1] + offset[1]) for point in outline]
    if len(outline) > 1:
        pygame.draw.lines(screen, color, True, outline, width)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Blit the track image
    screen.blit(track_image, (0, 0))

    # Draw the outline of the track
    draw_outline(screen, track_mask, offset=(0, 0), color=(255, 0, 0), width=2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
