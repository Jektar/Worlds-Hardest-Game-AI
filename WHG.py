import pysimpleGUI as GUI
import pygame as pg
import numpy as np
import random, sys
from settings import *
from blobs import BadBlobs
from player import Player
from loadWorld import loadWorld

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Worlds Hardest Game, played by AI')

clock = pg.time.Clock()


def main(ais=None, file='Maps/lvl2.txt', visuals=True, message='WHG', firstGreen=False):

    pg.display.set_caption(message)

    maxLength = len(ais[0])*(5//timePerInputAi) if ais != None else 9999999

    gameTics = 0

    startPos, walls, badBlobs, goal, checkPoints = loadWorld(file)
    checkPoints.append(goal)
    players = []
    if ais == None:
        players = [Player(startPos[0], startPos[1])]

    else:
        for ai in ais:
            players.append(Player(startPos[0], startPos[1], ai))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            for player in players:
                if ais == None:
                    player.getInput(event)


        for player in players:
            if ais != None:
                player.getAIMove(gameTics)

        for blob in badBlobs:
            blob.update()

        if visuals:

            screen.fill(GUI.WHITE)

            #Draw the walls
            for y, row in enumerate(walls):
                for x, wall in enumerate(row):
                    if wall == 1:
                        wallRect = pg.rect.Rect(x*tileSize, y*tileSize, tileSize, tileSize)
                        pg.draw.rect(screen, (128, 128, 255), wallRect)

                        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                            try:
                                if walls[y+direction[1]][x+direction[0]] == 0:
                                    if direction == (0, -1):
                                        #Up
                                        newRect = pg.Rect(wallRect.x, wallRect.y, tileSize, 5)
                                    elif direction == (0, 1):
                                        #Down
                                        newRect = pg.Rect(wallRect.x, wallRect.y+tileSize-5, tileSize, 5)

                                    elif direction == (-1, 0):
                                        #Left
                                        newRect = pg.Rect(wallRect.x, wallRect.y, 5, tileSize)

                                    elif direction == (1, 0):
                                        #Right
                                        newRect = pg.Rect(wallRect.x+tileSize-5, wallRect.y, 5, tileSize)

                                    elif direction == (-1, -1):
                                        #Top Left
                                        newRect = pg.Rect(wallRect.x, wallRect.y, 5, 5)

                                    elif direction == (-1, 1):
                                        #Bottom Left
                                        newRect = pg.Rect(wallRect.x, wallRect.y + tileSize-5, 5, 5)

                                    elif direction == (1, -1):
                                        #Top Right
                                        newRect = pg.Rect(wallRect.x+tileSize-5, wallRect.y, 5, 5)

                                    elif direction == (1, 1):
                                        #Bottom Right
                                        newRect = pg.Rect(wallRect.x+tileSize-5, wallRect.y+tileSize-5, 5, 5)

                                    pg.draw.rect(screen, (0, 0, 0), newRect)

                            except IndexError:
                                pass

                    elif wall == 0:
                        if (y+x)%2 == 0:
                            pg.draw.rect(screen, (200, 200, 255), (x*tileSize, y*tileSize, tileSize, tileSize))

            for checkPoint in checkPoints:
                pg.draw.rect(screen, (128, 255, 128), checkPoint)

            pg.draw.rect(screen, GUI.YELLOW, goal)

        for i, player in enumerate(players):
            # Update/move/collision detection for the players

            player.update(walls, badBlobs, checkPoints)
            if visuals:
                player.draw(screen)

        if visuals and firstGreen:
            players[0].draw(screen, color=GUI.GREEN)

        if visuals:
            for blob in badBlobs:
                blob.draw(screen)


        gameTics += 1
        if visuals:
            pg.display.update()
            clock.tick(FPS)
        if gameTics >= maxLength:
            return players, goal, checkPoints



if __name__ == '__main__':
    main()
