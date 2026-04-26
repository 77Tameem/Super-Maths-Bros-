import pygame



#load button images
start_image = pygame.image.load('graphics/start.png')
exit_image = pygame.image.load('graphics/exit.png')
back_image = pygame.image.load('graphics/back.png')


#Button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self,screen):
        action = False
        # get mouse postion
        pos = pygame.mouse.get_pos()
        
        
        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True 
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        
            
        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Function to create buttons (instead of defining them globally)
def create_buttons():
    start_button = Button(100, 200, start_image, 0.5)
    exit_button = Button(150, 350, exit_image, 0.5)
    back_button = Button (500, 600, back_image,0.25)
    return start_button, exit_button, back_button  # Return buttons instead of defining them globally