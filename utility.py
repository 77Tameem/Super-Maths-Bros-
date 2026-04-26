#This whole file is a utility file that contains functions to help with the main program.
import pygame

# This function scales an image by a given factor
# and returns the scaled image.
def scale_image(img, factor):
    #Scales an image by a given factor
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False 

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
    
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        
        moved = True
        player_car.move_backward()

    if not moved:
   
        player_car.reduce_speed()

def blit_text_center(screen, font, text):
    render = font.render(text, 1, (200, 200, 200))
    screen.blit(render, (screen.get_width() / 2 - render.get_width()/2 , screen.get_height()/2 - render.get_height()/2))
     