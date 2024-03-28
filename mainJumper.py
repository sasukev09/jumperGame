# importing libraries
import pygame
import random

# initialize pygame
pygame.init()

# Game window DIMENSIONS
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Game window CREATION
game_window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Jump Boi')

# Define color
WHITE = (255, 255, 255)

# Define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_medium = pygame.font.SysFont('Lucida Sans', 25)

# GAME Variables 
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESH = 200
scroll = 0
bg_scroll = 0
game_over = False
score = 0

# Load images 
dragon_image = pygame.image.load('assets/sasukevDragonNoB.png').convert_alpha()
bg_image = pygame.image.load('assets/galaxyBackground.png').convert_alpha()
ice_platform = pygame.image.load('assets/iceBlock.png').convert_alpha()

# Function for drawing the background
def draw_bg(bg_scroll):
    game_window.blit(bg_image, (0,0 + bg_scroll))
    game_window.blit(bg_image, (0,-600 + bg_scroll))
    
# Function for displaying text on screen
def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    game_window.blit(image, (x, y))

# Player class
class Player():
    #Constructor method
    def __init__(self, x,y):
        self.image =  pygame.transform.scale(dragon_image, (95, 120))
        self.width = 28
        self.height = 110
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
        self.velocity_y = 0
        self.flip = False

    # Drawing rectangle
    def draw(self):
        game_window.blit(pygame.transform.flip( self.image, self.flip, False), (self.rect.x -32, self.rect.y -8))
        pygame.draw.rect(game_window, WHITE, self.rect, 1) 
    
    # Move method
    def move(self):
        
        # Define scroll variable
        # Reset variables 'd' as in change in something
        dx = 0
        dy = 0 
        scroll = 0

        # Processing key presses
        key = pygame.key.get_pressed()
        # A and D keys are mapped
        if key[pygame.K_a]:
            dx = -8
            self.flip = False
        if key[pygame.K_d]:
            dx =  8
            self.flip = True
        # J and L keys are mapped
        if key[pygame.K_j]:
            dx = -8
            self.flip = False
        if key[pygame.K_l]:
            dx = 8
            self.flip = True

        # Gravity that pulls player down 
        self.velocity_y += GRAVITY
        dy += self.velocity_y

        # Make sure player does not go off the game screen
        #check collision to the left, i propose that i move by 8, so now I am saying
        #if I do move by 8, will I be off the edge which is x coordinate on the left = 0
        # if it less than 0 then reposition to a distance between the left side and the edge
        # -rect.dot.lenght is the distance between left side and edge
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        #Doing the same with the right side which = screen_width
        #if position gets off the edge, mantain me at this new dx position before the right edge of screen
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        
        # Check collision with ground / bottom edge of screen
        #if self.rect.bottom + dy > SCREEN_HEIGHT:
            #dy = 0
            #self.velocity_y = -22

        # Check collision with platforms
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if player is above the platform
                if self.rect.bottom < platform.rect.centery:
                    # is it jumping on platform or falling
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.velocity_y = -22

        # Check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            #If player is jumping
            if self.velocity_y < 0:
                scroll = -dy 

        # update rectangle positition
        self.rect.x += dx
        self.rect.y += dy + scroll 

        return scroll

# Platform class, using sprite classes, added in the arg to inherit
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(ice_platform, (width, 28))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll):
        #Update platforms vertical position
        self.rect.y += scroll

        #check if platform has gone of the screen, if so delete the platform
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Create sprite groups to store platforms
platform_group = pygame.sprite.Group()

# Create temporary platforms
#for plat in range(MAX_PLATFORMS):
    #plat_width = random.randint(40,60)
    #plat_x = random.randint(0, SCREEN_WIDTH- plat_width)
    #plat_y = plat * random.randint(80, 100)
    #platform = Platform(plat_x, plat_y, plat_width)
    #platform_group.add(platform)

#Create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 53, SCREEN_HEIGHT - 100, 100)
platform_group.add(platform)

# Defining the player INSTANCE in the game
dragon = Player(SCREEN_WIDTH // 2 , SCREEN_HEIGHT -150)

# Game's main loop, contains game logic inside loop
run =  True
while run:

    if game_over == False:
        # Scroll control where player moves
        scroll = dragon.move()
        print(scroll)

        # Draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        #print(bg_scroll)

        # Draw player sprite
        dragon.draw()

        #Draw platform sprite
        platform_group.draw(game_window)

        # Generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            platform_w = random.randint(40, 60)
            platform_x = random.randint(0, SCREEN_WIDTH - platform_w)
            platform_y = platform.rect.y - random.randint(80, 120)

            platform = Platform(platform_x, platform_y, platform_w)
            platform_group.add(platform)

        print(len(platform_group))

        # Draw temporary threshold
        #pygame.draw.line(game_window, WHITE, (0, SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))

        # Setting quickness/framerate of game
        clock.tick(FPS)

        # Update platforms
        platform_group.update(scroll)

        # GAME OVER condition
        if dragon.rect.top > SCREEN_HEIGHT:
            game_over = True

    else: 
        # Display message if 
        draw_text('GAME OVER', font_medium, WHITE, 150, 200)
        draw_text('YOUR SCORE: ' + str(score), font_medium, WHITE, 130, 270)
        draw_text('PRESS ENTER TO PLAY AGAIN', font_medium, WHITE, 50, 350)
        key = pygame.key.get_pressed()
        if key [pygame.K_RETURN]:
            #reset variables
            game_over = False
            score = 0
            scroll = 0
            #reposition player
            dragon.rect.center = (SCREEN_WIDTH // 2 , SCREEN_HEIGHT -150)
            #reset platforms
            platform_group.empty()
            #create platforms again
            platform = Platform(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT - 100, 50)
            platform_group.add(platform)


    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # At the end of loop, tell pygame to update the display window
    pygame.display.update()
pygame.quit()


# Show image onto the screen


