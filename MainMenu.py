import pygame
import time 
import math
import random
from utility import move_player
from utility import scale_image 
from utility import blit_rotate_center
from utility import blit_text_center
from sys import exit
import button
pygame.font.init()

# Made By Tameem Husayn
# Initialise pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Super Maths Bro')

# Set the framerate
clock = pygame.time.Clock()

# Assign the start buttons and exit buttons
start_button, exit_button, back_button = button.create_buttons()

# Load the background image for the main menu and other variables
background_surface = pygame.image.load('graphics/background.jpg')
GRASS = scale_image(pygame.image.load("graphics/grass.jpg"),2.5)
TRACK = scale_image(pygame.image.load("graphics/track.png"),1.5)

TRACK_BORDER = scale_image(pygame.image.load("graphics/track-border.png"),1.5)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = scale_image(pygame.image.load("graphics/finish.png"),0.5)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION  = (60, 170)

PURPLE_CAR = scale_image(pygame.image.load("graphics/purple-car.png"),0.3)
GREY_CAR = scale_image(pygame.image.load("graphics/grey-car.png"),0.3)
PATH = [(80, 287), (76, 512), (156, 663), (268, 680), (359, 609), (404, 686), (326, 737), (111, 742), (45, 704), (32, 565), (31, 292), (30, 120), (51, 59), (121, 34), (305, 26), (386, 63), (397, 178), (399, 331), (406, 441), (350, 538), (235, 611), (154, 547), (266, 427), (348, 333), (289, 281), (185, 376), (140, 311), (224, 229), (300, 207), (338, 151), (287, 89), (135, 81), (79, 130), (79, 172)]
WIDTH, HEIGHT = TRACK.get_width()+200, TRACK.get_height()
LEVEL = 10

MAIN_FONT = pygame.font.SysFont("comicsans", 44)
SUB_FONT = pygame.font.SysFont("comicsans", 25)
#Mouse position
pos = pygame.mouse.get_pos()

class GameInfo:
    LEVELS = 10

    #Indicates the level of the game is level 1 
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0
    #Allows the user to start the next level of the game
    def next_level(self):
        self.level += 1
        self.started = False
    #Resets the game
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS
    
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)
    
class AbstractCar:
   
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.angle = 180
        self.vel = 0
        self.x , self.y = self.START_POS
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.acceleration = 0.1
        
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, screen):
        blit_rotate_center(screen, self.img, (self.x, self.y), self.angle)    
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    #does the movements of the car using some trigonometry
    # The angle is converted to radians and the x and y coordinates are changed    
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
        

    # Slows down the car so it deosn't instantly stop deacceleration
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        #Point of intersection
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 180
        self.vel = 0
        self.current_point = 0


    




class PlayerCar(AbstractCar):
      IMG = PURPLE_CAR
      START_POS = (70, 200)

      def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

      def bounce(self):
        self.vel = -self.vel
        self.move()

def produce(screen, images, player_car, computer_car, game_info):
    for img, pos in images:
        screen.blit(img, pos)

      # Debug 
    level_text = MAIN_FONT.render(f"Level: {game_info.level}", 1, (255, 255, 255))
    screen.blit(level_text, (440, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    screen.blit(time_text, (420, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(f"VEL: {round(player_car.vel,1)}px/s", 1, (255, 255, 255))
    screen.blit(vel_text, (400, HEIGHT - vel_text.get_height() - 10))

    player_car.draw(screen)
    computer_car.draw(screen)
    pygame.display.update() 

#Handles all collision with the track border and the finish line.
def   handle_collision(player_car, computer_car,game_info):
    
        if player_car.collide(TRACK_BORDER_MASK) != None:
            player_car.bounce()


        computer_finish_poi_collide = computer_car.collide(FINISH_MASK , *FINISH_POSITION)
        if computer_finish_poi_collide !=  None:
           blit_text_center(screen, MAIN_FONT, f"You Lost!")
           pygame.display.update()
           pygame.time.wait(5000)
           game_info.reset()
           player_car.reset()
           computer_car.reset()
           
        player_finish_poi_collide = player_car.collide(FINISH_MASK , *FINISH_POSITION)
        if player_finish_poi_collide is not  None:
           if player_car.vel > 0: #Moving forward
                print('You have crossed the finish line!')
                player_car.reset()
                game_info.next_level()
                computer_car.next_level()
           else:
               player_car.bounce()



class ComputerCar(AbstractCar):
    IMG = GREY_CAR
    START_POS = (80, 200)

    def __init__(self, max_vel, rotation_vel, path = []):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel 

    def draw_points (self, screen):
        for point in self.path:
            pygame.draw.circle(screen, (255, 0, 0), point, 5)

    def draw(self, screen):
        super().draw(screen)
        #self.draw_points(screen) #This allowed me to make my computer path

    #Calulates the displacement between the current point and the next point in the computer path.
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x  
        y_diff = target_y - self.y 

        #Prevents dividing by zero when working out the tangent of the angle
        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        #IF the angle is more extreme than the current car postion adds pi to the angle so that the tangent angle goes to the next value.
        if target_y > self.y:
            desired_radian_angle += math.pi

        #Convert the angle to degrees and takes what ever our current angle is and subtracts it from the desired angle.Telling whether we should move left or right.
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
       
        #If  value of the angle is greater than 180 degrees, add or subtract 360 degrees to get the shortest angle.To avoid inefficeints paths.
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        #Prevents the difference of the angle from being less than -180 degrees.Which would prevent the computer car from stuttering and going above or below the target angle.
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
    
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
    # helps the computer car to move along the path by checking if the current point is reached and moving to the next point.
    def update_path_point(self):
        target_x, target_y = self.path[self.current_point]
        distance = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        # Define a tolerance radius (e.g., 10 pixels)
        if distance < 10:
            self.current_point += 1


    
    def move(self):
        if self.current_point >= len(self.path):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()

    def reset(self):
        super().reset()
        self.current_point = 0
        self.vel = self.max_vel

    def next_level(self):
        self.reset()
        #The computer car will increase by this amount every level.
        self.vel = self.max_vel + (LEVEL - 8) * 0.2
        
        
        
    

images = [(GRASS, (0,0)), (TRACK, (0,0)),  (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(4 , 4)
computer_car = ComputerCar(1, 4, PATH)


# Function to create the main menu
def mainmenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw the background image on the screen
        screen.blit(background_surface, (0, 0))

        # If the start button is clicked, call the Play function and exit the main menu loop
        if start_button.draw(screen):
            Play()  # Calls Play() to switch screens

        # Exit button
        if exit_button.draw(screen):
            pygame.quit()
            exit()

        # Update the display and control framerate
        pygame.display.update()
        clock.tick(60)

def ask_math_question():
    """Generate and display a math question. Return True/False and the correct answer."""
    num1 = random.randint(1, 12)
    num2 = random.randint(1, 12)
    correct_answer = num1 * num2

    # Display the question
    question_text = f"What is {num1} x {num2}?"
    player_answer = ""

    while True:
        screen.fill((0, 0, 0))  # Clear the screen
        blit_text_center(screen, MAIN_FONT, question_text)  # Display the question above the input
        answer_text = MAIN_FONT.render(player_answer, True, (255, 255, 255))
        screen.blit(answer_text, (WIDTH // 2 - answer_text.get_width() // 2, HEIGHT // 2 + 50))  # Display the input below the question
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to submit the answer
                    if player_answer.isdigit() and int(player_answer) == correct_answer:
                        return True, correct_answer  # Correct answer
                    else:
                        return False, correct_answer  # Incorrect answer
                elif event.key == pygame.K_BACKSPACE:  # Backspace to delete a character
                    player_answer = player_answer[:-1]
                else:
                    player_answer += event.unicode  # Add typed character to the answer




# Function to create the play screen
def Play():
    # Change window title when on the play screen
    pygame.display.set_caption('Play')
    start_button, exit_button, back_button = button.create_buttons()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_info = GameInfo()
    #Timer to delay the computer car when the player answers correctly
    #sets the intial value of the computer car delay to 0
    computer_car_delay = 0 
    #Boolean to check if the math question has been asked
    #This is used to prevent the math question from being asked multiple times in a level.
    math_question_asked = False

    while True:
        #Click the screen or press any button to start new level
        while not game_info.started:
            screen.fill((0, 0, 0))  # Clear the screen
            blit_text_center(screen, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            clock.tick(60)
            
            # Check for events to start the level
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    # Start the level when any key is pressed
                    game_info.start_level()
                    math_question_asked = False  # Reset the math question asked flag

        # Ask the math question after the level starts, but only once
        if not math_question_asked:
            correct, correct_answer = ask_math_question()
            if correct:
                # Display correct answer feedback
                screen.fill((0, 0, 0))
                blit_text_center(screen, MAIN_FONT, "Correct! You get a head start!")
                pygame.display.update()
                pygame.time.wait(1000)
                computer_car_delay = 5  # Delay the computer car for 5 seconds
            else:
                # Display "Incorrect!" feedback with the correct answer
                screen.fill((0, 0, 0))
                blit_text_center(screen, SUB_FONT, f"Incorrect! The correct answer is {correct_answer}.")
                pygame.display.update()
                pygame.time.wait(1000)  # Pause for 1 second
                
            # Ensure the question is not asked again
            math_question_asked = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                computer_car.path.append(pos)
                print(computer_car.path)  # Only print when a new point is added
             
    

        # Draw the game elements on the screen
        produce(screen, images, player_car,computer_car,game_info)

        # Draw the back button and handle its click
        if back_button.draw(screen):
            screen = pygame.display.set_mode((1280, 720))
            return
        
        #Move the player car based on key presses
        
        
        move_player(player_car)
        #Move the computer car along the path(finally works ;-;)
        # Delay the computer car's movement if the player answered correctly
        if computer_car_delay > 0:
            computer_car_delay -= 1 / clock.get_fps()  # Decrease delay based on frame rate
        else:
            computer_car.move()  # Allow the computer car to move after the delay


        #check for collisions with the track border and bounces the player car back
        
        handle_collision(player_car, computer_car,game_info)

        if game_info.game_finished():
            blit_text_center(screen, MAIN_FONT, f" You have won the game !")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.reset()



        #updates game display
        pygame.display.update()
        #Updates frame rate
        clock.tick(60)
        
        



# Start the game by running the mainmenu function
if __name__ == "__main__":
    mainmenu()