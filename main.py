import math
import time
import pygame
from random import *
from pygame.locals import *
from pprint import pprint
import copy
pygame.init()
FPS = 60  # frames per second setting
FPSCLOCK = pygame.time.Clock()
WHITE = (255,255,255)
BLACK = (0,0,0)

Purp1 = pygame.image.load("Purple1.png")
Slime = pygame.transform.scale(Purp1, (32, 24))

Purp2 = pygame.image.load("Purple2.png")
Slime2 = pygame.transform.scale(Purp2, (32, 24))

Purp1Left = pygame.image.load("Purp1Left.png")
Slime1Left = pygame.transform.scale(Purp1Left, (32, 24))

Purp2Left = pygame.image.load("Purp2Left.png")
Slime2Left = pygame.transform.scale(Purp2Left, (32, 24))

Purp1Right = pygame.image.load("Purp1Right.png")
Slime1Right = pygame.transform.scale(Purp1Right, (32, 24))

Purp2Right = pygame.image.load("Purp2Right.png")
Slime2Right = pygame.transform.scale(Purp2Right, (32, 24))

Purp1Up = pygame.image.load("Purp1Up.png")
Slime1Up = pygame.transform.scale(Purp1Up, (32, 24))

Purp2Up = pygame.image.load("Purp2Up.png")
Slime2Up = pygame.transform.scale(Purp2Up, (32, 24))

Shot = pygame.image.load("Shot.png")
Shot1 = pygame.transform.scale(Shot, (8, 8))

class Player(pygame.sprite.Sprite):
    def __init__(self,posX,posY, image,image2):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [posX,posY]
        self.timer = 0

    def update(self, posX, posY, image,image2):
        print(str(self.timer))
        self.rect.center = [posX,posY]
        if self.timer < 2:
            self.image = image
        if self.timer <4 and self.timer > 2:
            self.image = image2

        self.timer +=1
        if self.timer == 4:
            self.timer = 0

class Shot(pygame.sprite.Sprite):
    def __init__(self, posX, posY, posX2,posY2, image):
        super().__init__()
        self.X = posX
        self.Y = posY
        self.tX = posX-posX2
        self.tY = posY - posY2
        self.image = image

        self.tXDir = self.tX / (math.sqrt((self.tX * self.tX) + (self.tY * self.tY)) / 10)
        self.tYDir = self.tY / (math.sqrt((self.tX * self.tX) + (self.tY * self.tY)) / 10)
        self.X -= self.tXDir
        self.Y -= self.tYDir
        self.rect = self.image.get_rect()
        self.rect.center = [self.X, self.Y]


    def update(self):
        self.X -= self.tXDir
        self.Y -= self.tYDir
        self.rect.center = [self.X, self.Y]



class Board():
    def __init__(self):
        self.Width = 500
        self.Height = 500


    def drawSelect(self):
        screen.fill(WHITE)
        screen2.fill(BLACK)
        pygame.draw.rect(screen, BLACK, (25, 25, 450, 450), 5)


    def blitScreen(self, Width, Height):
        if Width > Height:
            screen2.blit(pygame.transform.scale(screen, (Height, Height)), ((Width - Height) / 2, 0))
        else:
            screen2.blit(pygame.transform.scale(screen, (Width, Width)), (0, (Height - Width) / 2))


def main():
    global screen,screen2
    running = True
    Left = False
    Right = False
    Up = False
    Down = False
    Dash = False
    Width = 500
    Height = 500
    xLoc = 250
    yLoc = 350
    mousex = 0
    mousey = 0
    mouseDown = False
    screen = pygame.Surface((Width, Height))
    screen2 = pygame.display.set_mode((Width, Height), RESIZABLE)
    board = Board()
    Speed = 3
    diaSpeed = math.sqrt(.5 * Speed ** 2)
    bulletTick = 0
    SlimeI1 = Slime
    SlimeI2 = Slime2

    player = Player(xLoc,yLoc, Slime,Slime2)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bulletG = pygame.sprite.Group()

    while running:

        for event in pygame.event.get():
            pygame.event.pump()


            if event.type == QUIT:
                running = False

            if event.type == VIDEORESIZE:
                Width = event.w
                Height = event.h
                board.blitScreen(Width, Height)

            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                bulletTick = 0
                mouseDown = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == ord('w'):
                    Up = True
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    Down = True
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    Left = True
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    Right = True

                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RCTRL:
                    Dash = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    Left = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    Right = False
                if event.key == pygame.K_UP or event.key == ord('w'):
                    Up = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    Down = False
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RCTRL:
                    Dash = False

        board.drawSelect()

        if mouseDown == True:
            bulletTick += 1
            if bulletTick % 1 == 0:
                if Width > Height:
                    shot = Shot(xLoc, yLoc, (mousex - ((Width - Height)/2))/(Height /500), mousey/(Height/500), Shot1)
                    bulletG.add(shot)
                else:
                    shot = Shot(xLoc, yLoc, mousex / (Width / 500), (mousey - ((Height - Width)/2))/(Width /500), Shot1)
                    bulletG.add(shot)
        if Left and Down or Left and Up or Right and Up or Right and Down:
            dia = True
        else:
            dia = False

        if dia == False:
            if Left == True and Right == False:
                if xLoc > 46 + Speed:
                    xLoc -= Speed
                else:
                    xLoc = 46
            if Right == True and Left == False:
                if xLoc < 454 - Speed:
                    xLoc += Speed
                else:
                    xLoc = 454
            if Up == True and Down == False:
                if yLoc > 42 + Speed:
                    yLoc -= Speed
                else:
                    yLoc = 42
            if Down == True and Up == False:
                if yLoc < 458 - Speed:
                    yLoc += Speed
                else:
                    yLoc = 458
        if dia == True:
            if Left == True and Right == False:
                if xLoc >46 + diaSpeed:
                    xLoc -= diaSpeed
                else:
                    xLoc = 46
            if Right == True and Left == False:
                if xLoc < 454 - diaSpeed:
                    xLoc += diaSpeed
                else:
                    xLoc = 454
            if Up == True and Down == False:
                if yLoc > 42 + diaSpeed:
                    yLoc -= diaSpeed
                else:
                    yLoc = 42
            if Down == True and Up == False:
                if yLoc < 458 - diaSpeed:
                    yLoc += diaSpeed
                else:
                    yLoc = 458


        if Up == True and Right == False and Left ==False:
            SlimeI1 = Slime1Up
            SlimeI2 = Slime2Up
        elif Left == True and Right == False:
            print('check')
            SlimeI1 = Slime1Left
            SlimeI2 = Slime2Left
        elif Right == True and Left == False:
            print('check')
            SlimeI1 = Slime1Right
            SlimeI2 = Slime2Right
        else:
            SlimeI1 = Slime
            SlimeI2 = Slime2



        player_group.update(xLoc, yLoc, SlimeI1,SlimeI2)
        player_group.draw(screen)

        bulletG.update()
        bulletG.draw(screen)

        board.blitScreen(Width, Height)
        pygame.display.update()
        FPSCLOCK.tick(60)


main()

