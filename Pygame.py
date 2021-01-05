#Sari Pagurek Pygame 2020
#Import library
import pygame
from pygame.locals import *
import time

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
win = 0


#Load sprites
background_one = pygame.image.load("data/background_CURVE2.png")
home = pygame.image.load("data/home1.png")
menu = pygame.image.load("data/levels1.png")
lose = pygame.image.load("data/lose1.png")

block_img = pygame.image.load("data/grass_CURVE.png")
diamond_img = pygame.image.load("data/diamond5.png")

#Functions
def fail():
    player.rect.x = 5
    player.rect.y = 1000
    screen.blit(lose, (0,0))
    #menu_button.draw(screen)

def win():
    pygame.time.wait(300)
    player.rect.x = 5
    player.rect.y = 1000
    screen.blit(lose, (0,0))
    #menu_button.draw(screen)

class Button():
    def __init__(self, color, hover_color, x, y, width, height, text, clicked):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.default_color = color
        self.hover_color = hover_color
        self.clicked = clicked
        #self.button_list

        #for button in button_list:
            #button = (img, img_rect) #store image and image rectangle in variable
            #self.tile_list.append(button) #Add variable^ to list

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('timesnewroman', 25)
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
        for tile in state.level.tile_list:
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
        #diamond collision
        if pygame.sprite.spritecollide(self, state.level.diamond_group, False):
            win()

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
    def __init__(self, data, image, buttons):
        self.data = data
        self.image = image
        self.tile_list = []
        self.buttons = buttons
        self.diamond_group = pygame.sprite.Group()

        rowNum = 0 #Count which row
        for row in data:
            columnNum = 0 #Count which column
            for tile in row:
                if tile == 1: #for each 1 in level_data, load block img
                     img = pygame.transform.scale(block_img, (tile_size, tile_size)) #scale to tile size
                     img_rect = img.get_rect() #Convert image size into rectangle
                     img_rect.x = columnNum * tile_size #Determine x & y coord using row/column * tile size
                     img_rect.y = rowNum * tile_size
                     tile = (img, img_rect, type) #store image and image rectangle in variable
                     self.tile_list.append(tile) #Add variable^ to list
                if tile == 2: #for each 1 in level_data, load block img
                     diamond = Diamond(columnNum * tile_size, rowNum * tile_size)
                     self.diamond_group.add(diamond)
                columnNum += 1 #increase row & column by one (loop)
            rowNum += 1
    def draw(self):
        screen.blit(self.image, (0,0))
        self.diamond_group.draw(screen)
        for button in self.buttons:
            button.draw(screen)

        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 0, 0), tile[1], 2)

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = diamond_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class State():
    def __init__(self, level):
        self.level = level

    def set_level(self, newLevel):
        self.level = newLevel
        return None

#Level data, where platform blocks are located
level_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
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

menu_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

level2_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
[1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
]

level3_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

level4_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
[0, 0, 0, 1, 0, 0, 1, 2, 0, 0],
[1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#display = home_data
#display = Display(home_data) ###
player = Player(x, y)
#diamond_group = pygame.sprite.Group()
#level = Level(home_data, home)
#start_button = Button((173, 131, 201), 290, 420, 400, 60, 'Start Game')
#home_button = Button((173, 131, 201), 20, 20, 60, 60, 'Home')
#menu_button = Button((173, 131, 201), 290, 420, 400, 60, 'Levels Menu')
#level1_button = Button((173, 131, 201), 300, 280, 400, 60, 'Level One')
#level2_button = Button((236, 111, 111), 300, 380, 400, 60, 'Level Two')
#level3_button = Button((159, 236, 105), 300, 480, 400, 60, 'Level Three')
#level4_button = Button((149, 218, 197), 300, 580, 400, 60, 'Level Four')

#button = [
#(start_button),
#(menu_button),
#(level1_button),
#(level2_button),
#(level3_button),
#(level4_button),
#]


def homeScreen():
    return Level(home_data, home, [
        Button((173, 131, 201), (146, 106, 173), 290, 420, 400, 60, 'Start Game', lambda state: (state.set_level(menuScreen()), print('clicked')))
    ])
def menuScreen():
    global level
    player.rect.x = x
    player.rect.y = y
    print('menu')
    return Level(menu_data, menu, [
        #Button((173, 131, 201), (146, 106, 173), 290, 420, 400, 60, 'Levels Menu', lambda: (level := menuScreen())),
        Button((173, 131, 201), (146, 106, 173), 300, 280, 400, 60, 'Level One', lambda state: (state.set_level(levelOne()))),
        Button((236, 111, 111), (210, 82, 82), 300, 380, 400, 60, 'Level Two', lambda state: (state.set_level(levelTwo()))),
        Button((159, 236, 105), (115, 187, 65), 300, 480, 400, 60, 'Level Three', lambda state: (state.set_level(levelThree()))),
        Button((149, 218, 197), (92, 185, 157), 300, 580, 400, 60, 'Level Four', lambda state: (state.set_level(levelFour()))),
    ])
def levelOne():
    player.rect.x = x
    player.rect.y = y
    return Level(level_data, background_one, [])
def levelTwo():
    player.rect.x = x
    player.rect.y = y
    return Level(level2_data, background_one, [])
def levelThree():
    player.rect.x = x
    player.rect.y = y
    return Level(level3_data, background_one, [])
def levelFour():
    player.rect.x = x
    player.rect.y = y
    return Level(level4_data, background_one, [])

state = State(homeScreen())
#Infinite loop
while 1:
    #clear the screen before drawing it again
    screen.fill(0)
    state.level.draw()
    #update the screen
    player.update()
    #level.diamond_group.draw(screen)

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
            for button in state.level.buttons:
                if button.hover(mousePosition):
                    button.clicked(state)

        if event.type == pygame.MOUSEMOTION:
            for button in state.level.buttons:
                if button.hover(mousePosition):
                    button.color = button.hover_color
                else:
                    button.color = button.default_color
