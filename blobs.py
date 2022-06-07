from settings import *
import math, copy
import pygame as pg
import numpy as np

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def euclideanDist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

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
        #print("Error: Points are not on the same line")
        pass
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

def getAngle(center, point):
    x, y = point
    x1, y1 = center
    return math.atan2(y-y1, x-x1)

def getPosFromAngle(distance, center, angle):
    x, y = center
    return (x + distance * math.cos(angle), y + distance * math.sin(angle))

blobImg = getImg('blob.png')

class BadCircleBlobs:
    def __init__(self, center, nBlobs, radius=tileSize//6):
        self.center = center
        self.radius = radius
        self.blobs = []
        for dir in directions:
            for i in range(nBlobs):
                self.blobs.append([self.center[0] + dir[0] * tileSize * (i+1), self.center[1] + dir[1] * tileSize * (i+1)])


    def update(self):
        for i, blob in enumerate(self.blobs):
            #Here we need math, and lots of it
            currentAngle = getAngle(self.center, blob)
            newAngle = currentAngle + circleBlobSpeed
            distance = euclideanDist(self.center, blob)
            newPos = getPosFromAngle(distance, self.center, newAngle)
            self.blobs[i] = newPos



    def checkCollisions(self, player):
        for blob in self.blobs:
            if self.checkIndividualCollisions(blob, player):
                return True

        return False

    def checkIndividualCollisions(self, blobCenter, player):
        rect = player.rect
        cx, cy = blobCenter[0], blobCenter[1]
        rx, ry = rect.x, rect.y
        width, height = rect.width, rect.height

        testX = cx
        testY = cy

        if (cx < rx):
            testX = rx  # Left edge
        elif (cx > rx + width):
            testX = rx + width  # Right edge

        if (cy < ry):
            testY = ry  # Top edge
        elif (cy > ry + height):
            testY = ry + height  # Bottom edge

        distX = cx - testX
        distY = cy - testY
        distance = math.sqrt(distX ** 2 + distY ** 2)

        return distance <= self.radius

    def draw(self, screen):
        for blob in self.blobs:
            screen.blit(blobImg, (blob[0], blob[1]))

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
        screen.blit(blobImg, (self.x-5, self.y-5))

