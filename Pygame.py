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
pygame.display.set_caption("Enchanted Jumper")
keys = pygame.key.get_pressed()
mousePosition = pygame.mouse.get_pos()

#Variables
x = 5
y = 623 #screenheight - tile_size - player.width
move_x = 5
tile_size = 100

#Load sprites
background_one = pygame.image.load("data/background_level1A.png")
background_oneB = pygame.image.load("data/background_CURVE2.png")
background_two = pygame.image.load("data/background_level2.png")
background_three = pygame.image.load("data/background_level3B.png")
background_four = pygame.image.load("data/background_level4B.png")
home = pygame.image.load("data/homeFinal1.png")
menu = pygame.image.load("data/levels1.png")
lose = pygame.image.load("data/lose1.png")
win = pygame.image.load("data/win.png")

block_img = pygame.image.load("data/grass_CURVE.png")
diamond_img = pygame.image.load("data/diamond5.png")
shroom1 = pygame.image.load("data/shroom1A.png")
shroom1Highlight = pygame.image.load("data/shroom1Highlight.png")
shroom3 = pygame.image.load("data/shroom3.png")
shroom3Highlight = pygame.image.load("data/shroom3Highlight.png")
homeButton = pygame.image.load("data/homeButton.png")
spike = pygame.image.load("data/spike2.png")

#Classes
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.Font("data/NewYork.ttf", 25)
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
        self.gravity = 0

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
        if self.gravity == 0:
            self.move_y += 1
            if self.move_y > 10:
                self.move_y = 10
            dy += self.move_y
            img = pygame.image.load("data/playerCURVE.png") #load sprite
            self.image = pygame.transform.scale(img, (55, 77)) #scale to tile_size
        elif self.gravity == 1:
            self.move_y += 1
            if self.move_y > 10:
                self.move_y = 10
            dy -= self.move_y
            img = pygame.image.load("data/playerFLIP.png") #load sprite
            self.image = pygame.transform.scale(img, (55, 77)) #scale to tile_size

            #diamond collision
        if pygame.sprite.spritecollide(self, state.level.diamond_group, False):
            state.level = winScreen()

        if pygame.sprite.spritecollide(self, state.level.spike_group, False):
            state.level = fail()

        #mushrooms
        if pygame.sprite.spritecollide(self, state.level.shroom1_group, False):
            self.gravity = 1
            shroom1 = pygame.image.load("data/shroom1Highlight.png")

        if pygame.sprite.spritecollide(self, state.level.shroom3_group, False):
            self.gravity = 0
            #shroom3.image = shroom3Highlight

        #player collision
        for tile in state.level.tile_list:
            #x collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
            #y collision
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                player_center = (self.rect.top + self.rect.bottom) / 2
                block_center = (tile[1].top + tile[1].bottom) / 2

                if player_center > block_center: #player is below block
                    dy = tile[1].bottom - self.rect.top
                    self.move_y = 0

                if player_center < block_center:# player is above block
                    dy = tile[1].top - self.rect.bottom
                    self.move_y = 0

        #update player location
        self.rect.x += dx
        self.rect.y += dy

        #falling off screen
        if self.rect.bottom > (screenheight + 20):
            state.level = fail()
        if self.rect.top < -100:
            state.level = fail()

        #draw Player
        screen.blit(self.image, self.rect)#draw player on screen

class Level():
    def __init__(self, data, image, buttons):
        self.data = data
        self.image = image
        self.tile_list = []
        self.buttons = buttons
        self.diamond_group = pygame.sprite.Group()
        self.shroom1_group = pygame.sprite.Group()
        #self.shroom2_group = pygame.sprite.Group()
        self.shroom3_group = pygame.sprite.Group()
        self.spike_group = pygame.sprite.Group()

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
                if tile == 2: #for each 1 in level_data, load diamond img
                     diamond = Diamond(columnNum * tile_size, rowNum * tile_size)
                     self.diamond_group.add(diamond)
                if tile == 3: #for each 1 in level_data, load green mushroom img
                     shroom1 = Shroom1(columnNum * tile_size, rowNum * tile_size)
                     self.shroom1_group.add(shroom1)
                if tile == 5: #for each 1 in level_data, load pink mushroom img
                     shroom3 = Shroom3(columnNum * tile_size, rowNum * tile_size)
                     self.shroom3_group.add(shroom3)
                if tile == 6: #for each 1 in level_data, load spike img
                     spike = Spike(columnNum * tile_size, rowNum * tile_size)
                     self.spike_group.add(spike)
                columnNum += 1 #increase row & column by one (loop)
            rowNum += 1
    def draw(self):
        screen.blit(self.image, (0,0))
        self.diamond_group.draw(screen)
        self.shroom1_group.draw(screen)
        self.shroom3_group.draw(screen)

        self.spike_group.update()
        self.spike_group.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = diamond_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Shroom1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = shroom1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Shroom3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = shroom3
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = spike
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.move_direction *= -1
            self.move_counter *= -1

class State():
    def __init__(self, level):
        self.level = level

    def set_level(self, newLevel):
        self.level = newLevel
        return None

#Level data, where platform blocks are located
level_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[0, 0, 0, 0, 0, 0, 0, 3, 0, 1],
[0, 0, 0, 5, 0, 0, 1, 1, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[1, 1, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
[0, 3, 1, 0, 0, 0, 0, 0, 0, 0],
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

win_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

level2_data = [
[0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 1, 0, 0, 0, 0, 5, 0],
[6, 0, 0, 3, 0, 0, 0, 1, 1, 0],
[1, 0, 0, 0, 0, 6, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 5, 0],
[1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
]

level7_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 0, 0, 0, 0, 0, 0, 5, 0],
[0, 0, 0, 0, 5, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 6, 0, 0, 0, 3, 0],
[0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
[0, 0, 3, 0, 0, 0, 1, 0, 2, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

level4_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[5, 0, 0, 1, 1, 1, 0, 0, 0, 0],
[0, 0, 6, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
[0, 3, 0, 1, 0, 0, 1, 2, 0, 0],
[1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
[0, 0, 0, 0, 0, 6, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 3, 0],
]

level5_data = [
[0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
[0, 0, 0, 1, 1, 1, 0, 0, 6, 0],
[3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 6, 5, 0, 0, 3, 0, 6, 0],
[0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
[0, 0, 3, 0, 0, 0, 0, 0, 0, 2],
[1, 1, 0, 0, 0, 1, 0, 0, 6, 0],
]

level6_data = [
[0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
[0, 2, 1, 1, 0, 0, 5, 0, 6, 0],
[1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
[0, 0, 3, 0, 6, 0, 0, 0, 0, 0],
[0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
]

level3_data = [
[0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[5, 0, 0, 0, 0, 0, 5, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
[0, 0, 6, 0, 0, 6, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 1, 0, 0, 3],
[0, 3, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 6, 0, 0, 0, 0, 0, 0, 0],
]

level8_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[0, 0, 0, 0, 6, 0, 0, 5, 0, 0],
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
[0, 3, 0, 0, 0, 0, 6, 0, 0, 3],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
]

blank_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

player = Player(x, y)

def homeScreen():
    player.gravity = 0
    player.rect.x = x
    player.rect.y = y
    return Level(home_data, home, [
        Button((173, 131, 201), (146, 106, 173), 290, 420, 400, 60, 'Start Game', lambda state: (state.set_level(menuScreen())))
    ])
def fail():
    player.gravity = 0
    player.rect.x = 5
    player.rect.y = 1000
    return Level(blank_data, lose, [
        Button((173, 131, 201), (146, 106, 173), 290, 420, 400, 60, 'Levels Menu', lambda state: (state.set_level(menuScreen()))),
        Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])

def winScreen():
    player.gravity = 0
    return Level(win_data, win, [
        Button((173, 131, 201), (146, 106, 173), 290, 420, 400, 60, 'Levels Menu', lambda state: (state.set_level(menuScreen()))),
        Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def menuScreen():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    screen.blit(homeButton, (5, 100))
    return Level(menu_data, menu, [
        Button((173, 131, 201), (146, 106, 173), 300, 280, 400, 60, 'Level One', lambda state: (state.set_level(levelOne()))),
        Button((236, 111, 111), (210, 82, 82), 300, 380, 400, 60, 'Level Two', lambda state: (state.set_level(levelTwo()))),
        Button((159, 236, 105), (115, 187, 65), 300, 480, 400, 60, 'Level Three', lambda state: (state.set_level(levelThree()))),
        Button((149, 218, 197), (92, 185, 157), 300, 580, 400, 60, 'Level Four', lambda state: (state.set_level(levelFour()))),
        Button((173, 131, 201), (146, 106, 173), 705, 610, 30, 30, '>', lambda state: (state.set_level(menuScreen2()))),
        Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def menuScreen2():
    player.gravity = 0
    return Level(menu_data, menu, [
        Button((149, 218, 197), (92, 185, 157), 300, 280, 400, 60, 'Level Five', lambda state: (state.set_level(levelFive()))),
        Button((159, 236, 105), (115, 187, 65), 300, 380, 400, 60, 'Level Six', lambda state: (state.set_level(levelSix()))),
        Button((236, 111, 111), (210, 82, 82), 300, 480, 400, 60, 'Level Seven', lambda state: (state.set_level(levelSeven()))),
        Button((173, 131, 201), (146, 106, 173), 300, 580, 400, 60, 'Level Eight', lambda state: (state.set_level(levelEight()))),
        Button((173, 131, 201), (146, 106, 173), 265, 610, 30, 30, '<', lambda state: (state.set_level(menuScreen()))),
        Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelOne():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level_data, background_one, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelTwo():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level2_data, background_two, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelThree():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level3_data, background_three, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelFour():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level4_data, background_four, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelFive():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level5_data, background_three, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelSix():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level6_data, background_two, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelSeven():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level7_data, background_four, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])
def levelEight():
    player.rect.x = x
    player.rect.y = y
    player.gravity = 0
    return Level(level8_data, background_one, [
    Button((236, 111, 111), (210, 82, 82), 5, 5, 50, 50, '<', lambda state: (state.set_level(homeScreen()))),
    ])

state = State(homeScreen())
#Infinite loop
while 1:
    #clear the screen before drawing it again
    screen.fill(0)
    state.level.draw()
    #update the screen
    player.update()
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
