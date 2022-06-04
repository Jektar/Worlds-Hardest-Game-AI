import pysimpleGUI as GUI
import pygame as pg
from settings import *
from pygame.locals import *
import sys, loadWorld

saveTo = 'Maps/lvl2.txt'

def empty(_):
    #This is the definition of useless, but we have to input a function to every button even if it has no direct effect
    #I would complain about this, but seeing as I made the gui-library, I feel that would be hipocritical
    pass

def createRect(p1, p2):
    extraX = 0
    extraY = 0

    if p1[1] > p2[1]:
        top = p2[1]
        bottom = p1[1]
        extraY = tileSize

    else:
        top = p1[1]
        bottom = p2[1]

    if p1[0] > p2[0]:
        left = p2[0]
        right = p1[0]
        extraX = tileSize

    else:
        left = p1[0]
        right = p2[0]

    rect = pg.Rect(left, top, right-left+extraX, bottom-top+extraY)
    return rect

def getRightTile(x, y, anchor):
    xGreater = int(x > anchor[0])
    yGreater = int(y > anchor[1])

    return (x//tileSize+xGreater)*tileSize, (y//tileSize+yGreater)*tileSize

def resetCheckPoints(_):
    global checkPoints
    checkPoints = []

def removeCheckPoint(_):
    global checkPoints
    if len(checkPoints) > 0:
        checkPoints.pop()

try:
    startPos, walls, badBlobs, goal, checkPoints = loadWorld.loadWorld(saveTo, convertBlobs=False)
    goalPreview = None
    goalAnchor = None
    currentBlob = 0
    newFile = False
except FileNotFoundError:
    newFile = True

def clear(_):
    global walls, badBlobs, goal, checkPoints, startPos, goalAnchor, goalPreview, currentBlob
    walls = [[1 for i in range(sizeX)] for j in range(sizeY)]

    goal = None
    goalPreview = None
    goalAnchor = None

    startPos = None

    checkPoints = []

    badBlobs = []
    currentBlob = 0

if newFile:
    clear(None)

def saveMap(_):
    global walls, badBlobs, goal, checkPoints, startPos, saveTo
    with open(saveTo, 'w') as f:
        #Probably definitly have to change this
        #All parameters should be global, not parameters
        f.write(';'.join([str(i) for i in startPos])+'\n')

        goalX, goalY, goalW, goalH = goal.topleft[0]//tileSize, goal.topleft[1]//tileSize, goal.width//tileSize, goal.height//tileSize
        f.write(str(goalX)+';'+str(goalY)+';'+str(goalW)+';'+str(goalH)+'\n')

        badBlobsString = '|'.join([';'.join([str(pos[0])+','+str(pos[1]) for pos in blob]) for blob in badBlobs])
        f.write(badBlobsString+'\n')

        checkPointsString = '|'.join([str(pos[0]//tileSize)+';'+str(pos[1]//tileSize) for pos in checkPoints])
        f.write(checkPointsString+'\n')

        for row in walls:
            f.write(''.join([str(tile) for tile in row])+'\n')

pg.init()

screen = pg.display.set_mode((WIDTH+180, HEIGHT))

pg.display.set_caption('Create the level. Currently saving to ' + saveTo)

gridLayout = GUI.Layout()

for i in range(0, sizeX+1):
    line = GUI.GUIRect((i*tileSize, 0), (1, sizeY*tileSize), (128, 128, 128), topleft=True)
    gridLayout.addShape(line)

for i in range(0, sizeY+1):
    line = GUI.GUIRect((0, i*tileSize), (sizeX*tileSize, 1), (128, 128, 128), topleft=True)
    gridLayout.addShape(line)

gridLayout.setSurface(screen)

interFace = GUI.Layout()
rects = [GUI.GUIRect([WIDTH+90, 25+i*50], (160, 40), (0, 255, 0)) for i in range(6)]

text = ['Walls', 'Floor', 'Blobs', 'Start', 'CheckP', 'Goal']
textBoxes = [GUI.TextBox((WIDTH+90, 25+i*50), (255, 255, 255), word) for i, word in enumerate(text)]

buttons = [GUI.Button(rect, empty, textBox=textBoxes[i]) for i, rect in enumerate(rects)]

selector = GUI.Selector(buttons, (0, 0, 0))

interFace.addSelector(selector)

#Save button
rect = GUI.GUIRect([WIDTH+90, 16+12*50], (160, 40), (0, 255, 0))
textBoxes = GUI.TextBox([WIDTH+90, 16+12*50], (255, 255, 255), 'Save')
button = GUI.Button(rect, saveMap, textBox=textBoxes)
interFace.addButton(button)

#Here we have a button that resets checkPoints
rect = GUI.GUIRect([WIDTH+90, 25+6*50], (160, 40), (255, 0, 0))
textBox = GUI.TextBox([WIDTH+90, 25+6*50], (255, 255, 255), 'Reset Checkpoints', font=GUI.tinyFont)
button = GUI.Button(rect, resetCheckPoints, textBox=textBox)
interFace.addButton(button)

#Her we have a button to remove the latest checkpoint
rect = GUI.GUIRect([WIDTH+90, 25+7*50], (160, 40), (255, 0, 0))
textBox = GUI.TextBox([WIDTH+90, 25+7*50], (255, 255, 255), 'Remove Checkpoint', font=GUI.tinyFont)
button = GUI.Button(rect, removeCheckPoint, textBox=textBox)
interFace.addButton(button)

#Clear button
rect = GUI.GUIRect([WIDTH+90, 16+11*50], (160, 40), (255, 0, 0))
textBox = GUI.TextBox([WIDTH+90, 16+11*50], (255, 255, 255), 'Clear')
button = GUI.Button(rect, clear, textBox=textBox)
interFace.addButton(button)

interFace.setSurface(screen)

##The ability to open a file?

isHolding = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if badBlobs != []:
                    currentBlob -= 1
                    if currentBlob < 0:
                        currentBlob = len(badBlobs)-1

            elif event.key == K_RIGHT:
                if badBlobs != []:
                    currentBlob += 1
                    if currentBlob >= len(badBlobs):
                        currentBlob = 0

            elif event.key == K_BACKSPACE:
                if badBlobs != []:
                    badBlobs.remove(badBlobs[currentBlob])
                    currentBlob -= 1
                    if currentBlob < 0:
                        currentBlob = 0

            elif event.key == K_r:
                if badBlobs != [] and len(badBlobs[currentBlob]) > 1:
                    badBlobs[currentBlob].pop()

            elif event.key == K_e:
                if not [] in badBlobs:
                    badBlobs.append([])
                    currentBlob = len(badBlobs)-1


        if event.type == MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            interFace.collide(pos)
            isHolding = True

            option = interFace.selectors[0].getOutput()

            if option == 2:
                if badBlobs != []:
                    centerPos = (pos[0]//tileSize)*tileSize+tileSize//2, (pos[1]//tileSize)*tileSize+tileSize//2
                    badBlobs[currentBlob].append(centerPos)

            elif option == 3:
                if pos[0] < WIDTH and pos[1] < HEIGHT:
                    startPos = pos

            elif option == 4:
                if pos[0] < WIDTH and pos[1] < HEIGHT:
                    rect = pg.Rect(pos[0]//tileSize*tileSize, pos[1]//tileSize*tileSize, tileSize, tileSize)
                    checkPoints.append(rect)

            elif option == 5:
                if pos[0] < WIDTH and pos[1] < HEIGHT:
                    if goalPreview == None:
                        goalAnchor = (pos[0]//tileSize)*tileSize, (pos[1] // tileSize)*tileSize
                        goalPreview = pg.Rect(goalAnchor[0], goalAnchor[1], tileSize, tileSize)
                    else:
                        p1 = goalAnchor
                        p2 = getRightTile(pos[0], pos[1], goalAnchor)
                        goalPreview = createRect(p1, p2)

                        goal = goalPreview
                        goalPreview = None

        if event.type == MOUSEBUTTONUP:
            isHolding = False

    option = interFace.selectors[0].getOutput()
    pos = pg.mouse.get_pos()
    if pos[0] < WIDTH and pos[1] < HEIGHT:
        if option == 0 and isHolding: #Walls
            walls[pos[1] // tileSize][pos[0] // tileSize] = 1

        elif option == 1 and isHolding: #Floor
            walls[pos[1]//tileSize][pos[0]//tileSize] = 0


        elif option == 5 and goalPreview != None: #Goal
            p1 = goalAnchor
            p2 = getRightTile(pos[0], pos[1], goalAnchor)

            goalPreview = createRect(p1, p2)

    screen.fill(GUI.WHITE)

    for y, row in enumerate(walls):
        for x, wall in enumerate(row):
            if wall == 1:
                wallRect = pg.rect.Rect(x * tileSize, y * tileSize, tileSize, tileSize)
                pg.draw.rect(screen, (128, 128, 255), wallRect)

                for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    try:
                        if walls[y + direction[1]][x + direction[0]] == 0:
                            if direction == (0, -1):
                                # Up
                                newRect = pg.Rect(wallRect.x, wallRect.y, tileSize, 5)
                            elif direction == (0, 1):
                                # Down
                                newRect = pg.Rect(wallRect.x, wallRect.y + tileSize - 5, tileSize, 5)

                            elif direction == (-1, 0):
                                # Left
                                newRect = pg.Rect(wallRect.x, wallRect.y, 5, tileSize)

                            elif direction == (1, 0):
                                # Right
                                newRect = pg.Rect(wallRect.x + tileSize - 5, wallRect.y, 5, tileSize)

                            elif direction == (-1, -1):
                                # Top Left
                                newRect = pg.Rect(wallRect.x, wallRect.y, 5, 5)

                            elif direction == (-1, 1):
                                # Bottom Left
                                newRect = pg.Rect(wallRect.x, wallRect.y + tileSize - 5, 5, 5)

                            elif direction == (1, -1):
                                # Top Right
                                newRect = pg.Rect(wallRect.x + tileSize - 5, wallRect.y, 5, 5)

                            elif direction == (1, 1):
                                # Bottom Right
                                newRect = pg.Rect(wallRect.x + tileSize - 5, wallRect.y + tileSize - 5, 5, 5)

                            pg.draw.rect(screen, (0, 0, 0), newRect)

                    except IndexError:
                        pass

            elif wall == 0:
                if (y + x) % 2 == 0:
                    pg.draw.rect(screen, (200, 200, 255), (x * tileSize, y * tileSize, tileSize, tileSize))

    if goalPreview != None:
        pg.draw.rect(screen, (128, 255, 128), goalPreview)

    if goal != None:
        pg.draw.rect(screen, (0, 255, 0), goal)

    for checkPoint in checkPoints:
        pg.draw.rect(screen, (128, 255, 128), checkPoint)

    gridLayout.draw()

    if startPos != None:
        pg.draw.circle(screen, (255, 0, 0), startPos, 5)

    if badBlobs != []:
        for i, blob in enumerate(badBlobs):
            if blob != []:
                if i == currentBlob and option == 2:
                    pg.draw.circle(screen, (0, 0, 255), blob[0], 7)
                    for blob in blob[1:]:
                        pg.draw.circle(screen, (0, 0, 255), blob, 5)
                else:
                    pg.draw.circle(screen, (120, 120, 150), blob[0], 5)


    interFace.draw()
    pg.display.update()