from settings import *
import pygame as pg
from blobs import *

def intList(l):
    return [int(i) for i in l]

def loadWorld(worldFile, convertBlobs=True):
    with open(worldFile, 'r') as f:
        world = f.read()
        world = world.split('\n')
        startPos = [int(i) for i in world[0].split(';')]

        goalPos = [int(i) for i in world[1].split(';')]
        goal = pg.Rect(goalPos[0]*tileSize, goalPos[1]*tileSize, goalPos[2]*tileSize, goalPos[3]*tileSize)

        blobs = []
        if convertBlobs:
            if world[2] != '':
                for blob in world[2].split('|'):
                    corners = blob.split(';')
                    corners = [intList(corner.split(',')) for corner in corners]
                    blobs.append(BadBlobs(corners))

            if world[3] != '':
                for blob in world[3].split('|'):
                    center, nBlobs = blob.split(';')[0], blob.split(';')[1]
                    center = intList(center.split(','))
                    nBlobs = int(nBlobs)
                    blobs.append(BadCircleBlobs(center, nBlobs))


        else:
            if world[2] != '':
                for blob in world[2].split('|'):
                    corners = blob.split(';')
                    corners = [intList(corner.split(',')) for corner in corners]
                    blobs.append(corners)

            if world[3] != '':
                for blob in world[3].split('|'):
                    center, nBlobs = blob.split(';')[0], blob.split(';')[1]
                    center = intList(center.split(','))
                    nBlobs = int(nBlobs)
                    blobs.append([center, nBlobs])

        checkPoints = []
        if world[4] != '':
            for checkPoint in world[4].split('|'):
                position = [int(i) * tileSize for i in checkPoint.split(';')]
                rect = pg.Rect(position[0], position[1], tileSize, tileSize)
                checkPoints.append(rect)

        ##Walls
        walls = []
        for row in world[5:]:
            row = intList(list(row))
            walls.append(row)

    return startPos, walls, blobs, goal, checkPoints