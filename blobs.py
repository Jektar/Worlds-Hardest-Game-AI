from settings import *
import math, copy
import pygame as pg

def getImg(imgName):
    img = pg.image.load('Sprites/'+imgName)
    img = pg.transform.scale(img, (10, 10))
    return img

def getAllPointsInLine(start, end, step=1):
    x1, y1 = start
    x2, y2 = end
    points = []
    if x1 == x2:
        if y1 > y2:
            step *= -1

        for y in range(y1, y2, step):
            points.append((x1, y))

    elif y1 == y2:
        if x1 > x2:
            step *= -1

        for x in range(x1, x2, step):
            points.append((x, y1))
    else:
        print("Error: Points are not on the same line")
    return points

def createBlobPath(corners, blobspeed=5):
    path = []
    for i, corner in enumerate(corners):

        #corner contains position of the corner
        try:
            next = corners[i+1]
        except IndexError:
            next = corners[0]

        points = getAllPointsInLine(corner, next, step=blobspeed)
        path += copy.deepcopy(points)

    return path

blob = getImg('blob.png')

class BadBlobs:
    def __init__(self, travelPath, radius=tileSize//6):
        self.x = travelPath[0][0]
        self.y = travelPath[0][1]
        self.tics = 0
        self.travelPath = createBlobPath(travelPath)
        self.radius = radius

    def update(self):
        self.tics += 1
        if self.tics >= len(self.travelPath):
            self.tics = 0

        self.x = self.travelPath[self.tics][0]
        self.y = self.travelPath[self.tics][1]

    def checkCollisions(self, player):
        #Collision detection between player and badBlobs
        rect = player.rect
        cx, cy = self.x, self.y
        rx, ry = rect.x, rect.y
        width, height = rect.width, rect.height

        testX = cx
        testY = cy

        if (cx < rx): testX = rx #Left edge
        elif (cx > rx+width): testX = rx+width #Right edge

        if (cy < ry): testY = ry #Top edge
        elif (cy > ry+height): testY = ry+height #Bottom edge

        distX = cx - testX
        distY = cy - testY
        distance = math.sqrt(distX**2 + distY**2)

        return distance <= self.radius

    def draw(self, screen):
        screen.blit(blob, (self.x-5, self.y-5))

