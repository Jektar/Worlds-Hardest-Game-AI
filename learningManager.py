import random, WHG, copy
from settings import *

possibleInputs = [None, 'left', 'right', 'up', 'down']

def crossover(p1, p2, genNum, asexual=False):
    newModel = []

    #Get random from parents (maybe don't do this and only choose one parent?)
    if asexual:
        newModel = random.choice([p1, p2])
        newModel = copy.deepcopy(newModel)
    else:
        for i in range(len(p1)):
            if random.random() < 0.5:
                newModel.append(p1[i])
            else:
                newModel.append(p2[i])

    if random.random() < 0.5:
        index = random.randint(0, len(newModel)-1)
        newModel[index] = random.choice(possibleInputs)

    for i in range(random.randint(0, 5*timePerInputAi)):
        index = random.randint(len(newModel)-20, len(newModel)-1)
        newModel[index] = random.choice(possibleInputs)

    if genNum%10 == 0 and genNum != 0:
        for i in range(5*timePerInputAi):
            newModel.append(random.choice(possibleInputs))


    return newModel

def euclidDistance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def scorePlayer(player, goal, checkPoints, gen, map):
    score = 0
    currentGoal = checkPoints[player.accivedCheckPoints+1]

    if player.hasWon:
        #Has won
        score += 9999999
        saveModel(player.ai, 'bestModel.txt')
        WHG.main([player.ai], message='Winning in generation: '+str(gen), visuals=True, firstGreen=True, file=map)

        import sys
        sys.exit()

    if not player.alive and not player.hasWon:
        #Is dead
        score -= 9999999

    score += player.accivedCheckPoints*99999

    score -= euclidDistance(player.rect.center, currentGoal.center)/100

    return score

def scoreModels(models, gen, map):
    players, goal, checkPoints = WHG.main(models, message='Generation: '+str(gen), visuals=False, file=map)
    scores = [scorePlayer(player, goal, checkPoints, gen, map) for player in players]

    return scores

def saveModel(model, fileName):
    with open(fileName, 'w') as f:
        strModel = ';'.join([str(i)for i in model])
        f.write(strModel)

def transform(string):
    if string == 'None':
        return None
    else:
        return string

def loadModel(fileName):
    with open(fileName, 'r') as f:
        model = f.read()
        model = model.split(';')
        model = [transform(i) for i in model]
        return model

def trainModel(generations=1000, nModels=100, survivingPop=0.1, showEvery=20, map='Maps/lvl1.txt'):
    #We start with 20 inputs and after ten generations we add five more
    models = [[random.choice(possibleInputs) for i in range(20*timePerInputAi)] for n in range(nModels)]

    overAllBest = models[0]
    bestScore = -99999999

    for i in range(generations):

        scores = scoreModels(models, i, map)

        models = sorted(models, key=lambda x: scores[models.index(x)], reverse=True)
        scores = sorted(scores, reverse=True)

        if i%showEvery == 0:
            WHG.main(models, message='Generation: '+str(i), visuals=True, firstGreen=True)

        best = models[:int(survivingPop*nModels)]

        if scores[0] > bestScore:
            bestScore = scores[0]
            overAllBest = models[0]

        newModels = []
        while len(newModels) < nModels:
            p1 = random.choice(best)
            p2 = random.choice(best)
            newModels.append(crossover(p1, p2, i, asexual=True))

        models = newModels

    saveModel(overAllBest, 'bestModel.txt')
    return models

if __name__ == '__main__':
    trainModel()