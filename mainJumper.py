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

# GAME Variables 
GRAVITY = 1
MAX_PLATFORMS = 10

# Load images 
dragon_image = pygame.image.load('assets/sasukevDragonNoB.png').convert_alpha()
bg_image = pygame.image.load('assets/galaxyBackground.png').convert_alpha()
ice_platform = pygame.image.load('assets/iceBlock.png').convert_alpha()

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

        # Reset variables 'd' as in change in something
        dx = 0
        dy = 0 

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
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.velocity_y = -22

        # Check collision with platforms

        # update rectangle positition
        self.rect.x += dx
        self.rect.y += dy

# Platform class, using sprite classes, added in the arg to inherit
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(ice_platform, (width, 28))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups to store platforms
platform_group = pygame.sprite.Group()

# Create temporary platforms
for plat in range(MAX_PLATFORMS):
    plat_width = random.randint(40,60)
    plat_x = random.randint(0, SCREEN_WIDTH- plat_width)
    plat_y = plat * random.randint(80, 120)
    platform = Platform(plat_x, plat_y, plat_width)
    platform_group.add(platform)

# Defining the player INSTANCE in the game
dragon = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT -150)

# Game's main loop, contains game logic inside loop
run =  True
while run:
    # Draw game background
    game_window.blit(bg_image, (0,0))

    # Draw player sprite
    dragon.draw()

    #Draw platform sprite
    platform_group.draw(game_window)

    # Draw move method
    dragon.move()

    # Setting quickness/framerate of game
    clock.tick(FPS)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # At the end of loop, tell pygame to update the display window
    pygame.display.update()
pygame.quit()


# Show image onto the screen


