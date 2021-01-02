#Sari Pagurek Pygame 2020
#Import library
import pygame
from pygame.locals import *

#Set Up
pygame.init()
screenwidth = 1000
screenheight = 800
screen=pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Sari Pagurek Pygame")
keys = pygame.key.get_pressed()
mousePosition = pygame.mouse.get_pos()

#Variables
x = 5
y = 623 #screenheight - tile_size - player.width
move_x = 5
tile_size = 100



#Load sprites
background_one = pygame.image.load("data/background_CURVE2.png")
home = pygame.image.load("data/homeTest.png")
menu = pygame.image.load("data/levels.png")
lose = pygame.image.load("data/lose4.png")

#Functions
def fail():
    screen.blit(lose, (0,0))

class Button():
    def __init__(self, color, x, y, width, height, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def hover(self, mousePosition): #pos is variable storing mouse x&y
        if mousePosition[0] > self.x and mousePosition[0] < self.x + self.width:
            if mousePosition[1] > self.y and mousePosition[1] < self.y + self.height:
                return True
        return False

class Player():
    def __init__(self, x, y):
        img = pygame.image.load("data/playerCURVE.png") #load sprite
        self.image = pygame.transform.scale(img, (55, 77)) #scale to tile_size
        self.rect = self.image.get_rect() #convert img dimensions to rectangle
        self.rect.x = x #assign x & y coords of player to x/y of img rect
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_y = 0
        self.jumped = False

    def update(self):
        #change delta x/y with arrow keys
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False and self.rect.y > move_x:
            self.move_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT] and self.rect.x > move_x:
            dx -= move_x
        if key[pygame.K_RIGHT] and self.rect.x < screenwidth - (move_x + self.width):
            dx += move_x

        #gravity
        self.move_y += 1
        if self.move_y > 10:
            self.move_y = 10
        dy += self.move_y

        #player collision
        for tile in level.tile_list:
            #x collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #y collision
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #if collision above (jumping)
                if self.move_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.move_y = 0 #don't stick to bottom of blocks
                #if collision below (falling)
                elif self.move_y > 0:
                    dy = tile[1].top - self.rect.bottom
                    self.move_y = 0

        #update player location
        self.rect.x += dx
        self.rect.y += dy

        #falling off screen
        if self.rect.bottom > screenheight:
            fail()

        #draw Player
        screen.blit(self.image, self.rect)#draw player on screen
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

class Level():
    def __init__(self, data, image):
        self.data = data
        self.image = image
        self.tile_list = []
        #Load platform block sprite
        block_img = pygame.image.load("data/grass_CURVE.png")

        rowNum = 0 #Count which row
        for row in data:
            columnNum = 0 #Count which column
            for tile in row:
                if tile == 1: #for each 1 in level_data, load block img
                     img = pygame.transform.scale(block_img, (tile_size, tile_size)) #scale to tile size
                     img_rect = img.get_rect() #Convert image size into rectangle
                     img_rect.x = columnNum * tile_size #Determine x & y coord using row/column * tile size
                     img_rect.y = rowNum * tile_size
                     tile = (img, img_rect) #store image and image rectangle in variable
                     self.tile_list.append(tile) #Add variable^ to list
                columnNum += 1 #increase row & column by one (loop)
            rowNum += 1
    def draw(self):
        if self.data == level_data:
            #screen.fill(0)
            screen.blit(self.image, (0,0))
        elif self.data == home_data:
            #screen.fill(0)
            screen.blit(self.image, (0,0))
            start_button.draw(screen)

        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 0, 0), tile[1], 2)


#Level data, where platform blocks are located
level_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
]

home_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#display = home_data
#display = Display(home_data) ###
player = Player(x, y)
#level = Level(home_data, home)
start_button = Button((255, 0, 0), 400, 400, 200, 100, 'Start Game')

def homeScreen():
    return Level(home_data, home)

def levelOne():
    return Level(level_data, background_one)

level = homeScreen()
#Infinite loop
while 1:
    #clear the screen before drawing it again
    screen.fill(0)
    level.draw()
    #update the screen
    player.update()
    
    #display.update()
    pygame.display.update()
    #loop through the events
    for event in pygame.event.get():
        mousePosition = pygame.mouse.get_pos()
        #quit if X button
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.hover(mousePosition):
                print('clicked button')
                level = levelOne()
        if event.type == pygame.MOUSEMOTION:
            if start_button.hover(mousePosition):
                start_button.color = (0, 255, 0)
            else:
                start_button.color = (255, 0, 0)
