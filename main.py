import numpy as np
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import random
from itertools import groupby, product
import time
import threading
import csv



def Manhattan(tup1, tup2):
    return abs(tup1[0] - tup2[0]) + abs(tup1[1] - tup2[1])


def isNotLimited(value):
    try:
        if(1<value and value<limit-1):
            return True
    except:
        return False

def getSurronding(x,y):
    return [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]

def createShelter(center):
    for x_offsset  in range(-4, 4):
        for y_offsset in range(-4, 4):
            valueX=center[0]+x_offsset
            valueY=center[1]+y_offsset
            mapGame[valueX,valueY] = 1
            definedPoints.append([valueX, valueY])
            visitedPoints.append([valueX, valueY])
            defaultPoints.append([valueX, valueY])

    for x_offsset in range(-4 - saveZone, 4 + saveZone):
        for y_offsset in range(-4 - saveZone, 4 + saveZone):
            try:
                valueX=center[0]+x_offsset
                valueY=center[1]+y_offsset
                notAvailablePoints.append([valueX, valueY])
            except:
                pass

def createArena(center):
    for x_offsset  in range(-4, 4):
        for y_offsset in range(-4, 4):
            valueX=center[0]+x_offsset
            valueY=center[1]+y_offsset
            mapGame[valueX,valueY] = 1
            definedPoints.append([valueX, valueY])
            visitedPoints.append([valueX, valueY])
            defaultPoints.append([valueX, valueY])

    for x_offsset in range(-4 - saveZone, 4 + saveZone):
        for y_offsset in range(-4 - saveZone, 4 + saveZone):
            try:
                valueX = center[0] + x_offsset
                valueY = center[1] + y_offsset
                notAvailablePoints.append([valueX, valueY])
            except:
                pass

def createFountain():
    center = [np.random.randint(4, limit-4), np.random.randint(4, limit-4)]
    while center in notAvailablePoints:
        center = [np.random.randint(4, limit - 4), np.random.randint(4, limit - 4)]
    for x_offsset  in range(-2, 2):
        for y_offsset in range(-2, 2):
            valueX=center[0]+x_offsset
            valueY=center[1]+y_offsset
            mapGame[valueX,valueY] = 1
            definedPoints.append([valueX, valueY])
            visitedPoints.append([valueX, valueY])
            defaultPoints.append([valueX, valueY])


def initMap():
    createShelter([7,7])
    createShelter([7,43])
    createShelter([43,25])
    createArena([22,25])
    createFountain()
def createMap( id):
    targetPoint = [np.random.randint(1, limit-1), np.random.randint(1, limit-1)]
    while targetPoint in definedPoints:
        targetPoint = [np.random.randint(1, limit - 1), np.random.randint(1, limit - 1)]
    mapGame[targetPoint[0], targetPoint[1]] = 1
    toVisitPoint.append(targetPoint)
    while toVisitPoint:
        targetPoint=toVisitPoint.pop(0)
        targetX, targetY = targetPoint[0], targetPoint[1]
        xLimited = isNotLimited(targetX)
        yLimited = isNotLimited(targetY)
        if (xLimited and yLimited):
            values = getSurronding(targetPoint[0], targetPoint[1])
            emptyNearbyCels = 0
            blackCells = []
            for value in values:
                if not (value in definedPoints):
                    cellValue = np.random.randint(0, 2)
                    mapGame[value[0], value[1]] = cellValue
                    definedPoints.append(value)
                    if cellValue == 1:
                        emptyNearbyCels += 1
                        if (not (value in visitedPoints)):
                            toVisitPoint.append(value)
                    else:
                        blackCells.append(value)

            if emptyNearbyCels < 1:
                try:
                    toBeChanged = random.choice(blackCells)
                    mapGame[toBeChanged[0], toBeChanged[1]] = 1
                    if (targetPoint != toBeChanged):
                        toVisitPoint.append(toBeChanged)
                except:
                    print()

        visitedPoints.append(targetPoint)
    return targetPoint

if __name__ == "__main__":
    limit = 50
    np.set_printoptions(threshold=sys.maxsize)
    mapGame = np.zeros((limit, limit))
    saveZone = 7
    definedPoints = []
    defaultPoints = []
    visitedPoints = []
    toVisitPoint = []
    notAvailablePoints = []
    start_time = time.time()
    initMap()
    initial = createMap(1)

    # both threads completely executed
    print("--- %s seconds taken to create map ---" % (time.time() - start_time))
    '''
    start_time = time.time()
    openRow, openColumn = np.where(mapGame == 1)
    orderedOpenColumn = np.argsort(openColumn)
    points = np.vstack((openRow, openColumn)).T
    # Group Adjacent Coordinates
    # Using product() + groupby() + list comprehension
    man_tups = [sorted(sub) for sub in product(tuple(map(tuple,points)), repeat=2)
                if Manhattan(*sub) == 1]
    
    res_dict = {ele: {ele} for ele in tuple(map(tuple,points))}
    for tup1, tup2 in man_tups:
        res_dict[tup1] |= res_dict[tup2]
        res_dict[tup2] = res_dict[tup1]
    
    res = [[*next(val)] for key, val in groupby(
        sorted(res_dict.values(), key=id), id)]
    print(len(res))
    for i in range(0,len(res)):
        value = np.random.randint(100,len(res)+1000)
        for a in range(0,len(res[i])):
            x=res[i][a][0]
            y=res[i][a][1]
            mapGame[x,y] = value
    
    print("--- %s seconds taken to compute routes in map ---" % (time.time() - start_time))
    '''
    for point in defaultPoints:
        mapGame[point[0],point[1]]=2

    ax = sns.heatmap(mapGame, xticklabels=False, yticklabels=False, cbar=False)
    with open("map.csv", "w") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(mapGame)
        print("created map")
    plt.show()
    plt.pause(0.001)


