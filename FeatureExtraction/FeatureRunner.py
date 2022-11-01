import DataExtraction.FlatCharacterObject
from AllFeaturesProcessor import AllFeaturesProcessor
import numpy as np
import pandas as pd
from DataExtraction import *

def main():
    characterList = DataExtraction.FlatCharacterObject.readFile("../DataExtraction/characters.txt")
    dictOfCharacters = {}
    for character in characterList:
        if character.label not in dictOfCharacters:
            dictOfCharacters[character.label] = []
        dictOfCharacters[character.label].append(character)
    characterList = []

    allFeaturesProcessor = AllFeaturesProcessor()
    for label in dictOfCharacters:
        array = dictOfCharacters[label][0].get_array()
        featureValues, labels = allFeaturesProcessor.getAllDerivedFeaturesAndLabels(array)
        print(label)
        print(labels)
        print(featureValues)
        x_intersects, y_intersects = getIntersects(array, 2)
        print("X-intersects")
        print(x_intersects)
        print("Y-intersects")
        print(y_intersects)

def getIntersects(pic, numSamples):
    height = pic.shape[0]
    width = pic.shape[1]
    deltaHeight = height // numSamples
    deltaWidth = width // numSamples
    xIntersects = []
    yIntersects = []
    for i in range(0, height, deltaHeight):
        one = False
        count = 0
        for j in range(width):
            if pic[i][j] == 1 and one == False:
                one = True
                count += 1
            elif pic[i][j] == 0 and one == True:
                one = False
        xIntersects.append(count)
    for i in range(0, width, deltaWidth):
        one = False
        count = 0
        for j in range(height):
            if pic[j][i] == 1 and one == False:
                one = True
                count += 1
            elif pic[j][i] == 0 and one == True:
                one = True
        yIntersects.append(count)
    return xIntersects, yIntersects

if __name__ == "__main__":
    main()