from settings import *
from pygame.locals import *
import pygame as pg
import pysimpleGUI as GUI

directions = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
directionInputs = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}
keyTranslations = {K_w: 'w', K_s: 's', K_a: 'a', K_d: 'd'}

def getImg(imgName):
    img = pg.image.load('Sprites/'+imgName)
    img = pg.transform.scale(img, (tileSize-5, tileSize-5))
    return img

playerImg = getImg('player.png')
greenPlayerImg = getImg('greenPlayer.png')

class Player:
    def __init__(self, x, y, ai=None, speed=3):
        self.rect = pg.Rect(x, y, tileSize-5, tileSize-5)
        self.rect.center = (x, y)
        self.alive = True
        self.hasWon = False
        self.ai = ai #Just a vector of directions
        self.dir = None
        self.speed = speed
        self.accivedCheckPoints = -1

    def getAIMove(self, gameTics):
        input = gameTics//5
        self.dir = self.ai[input] #This can be None!

    def getInput(self, event):
        if event.type == KEYDOWN:
            try:
                key = keyTranslations[event.key]
                if key in ['w', 's', 'a', 'd']:
                    self.dir = directionInputs[key]
            except KeyError:
                pass

        if event.type == KEYUP:
            try:
                key = keyTranslations[event.key]
                if key in ['w', 's', 'a', 'd'] and self.dir == directionInputs[key]:
                    self.dir = None
            except KeyError:
                pass

    def checkCollisions(self, walls, enemies, checkPoints):
        currentGoal = checkPoints[self.accivedCheckPoints+1]
        if self.rect.colliderect(currentGoal) or (self.ai == None and self.rect.colliderect(checkPoints[-1])):
            self.accivedCheckPoints += 1
            if self.accivedCheckPoints == len(checkPoints)-1:
                self.hasWon = True
                self.alive = False
                self.accivedCheckPoints = -1

        gridPos = (self.rect.center[0]//tileSize, self.rect.center[1]//tileSize)

        relevantWalls = [(gridPos[0] + i, gridPos[1] + j) for i in range(-1, 2) for j in range(-1, 2)]

        for wall in relevantWalls:
            if walls[wall[1]][wall[0]] == 1: #Possibly some trouble with the y-axis here
                wallRect = pg.Rect(wall[0]*tileSize, wall[1]*tileSize, tileSize, tileSize)
                if self.rect.colliderect(wallRect):
                    #adjust posistion so that it doesn't overlap the wall
                    if self.dir == 'up':
                        self.rect.top = wallRect.bottom
                    elif self.dir == 'down':
                        self.rect.bottom = wallRect.top
                    elif self.dir == 'left':
                        self.rect.left = wallRect.right
                    elif self.dir == 'right':
                        self.rect.right = wallRect.left
                    self.dir = None

        for enemy in enemies:
            if enemy.checkCollisions(self):
                self.alive = False


    def update(self, walls, enemies, goal):
        if self.alive:
            self.move()
            self.checkCollisions(walls, enemies, goal)

    def move(self):
        if self.alive and self.dir != None:
            change = directions[self.dir]
            self.rect.center = (self.rect.center[0] + change[0] * self.speed, self.rect.center[1] + change[1] * self.speed)


    def draw(self, surface, color=GUI.RED):
        if self.alive:
            if color == GUI.RED:
                surface.blit(playerImg, self.rect)
            else:
                surface.blit(greenPlayerImg, self.rect)