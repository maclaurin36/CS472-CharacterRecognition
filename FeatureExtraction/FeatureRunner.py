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

    allFeaturesProcessor = AllFeaturesProcessor()
    len_intersects = 2

    allOutputs = []
    header = []
    for label in dictOfCharacters:
        for dictLabel in dictOfCharacters[label]:
            array = dictLabel.get_array()
            featureValues, labels = allFeaturesProcessor.getAllDerivedFeaturesAndLabels(array)
            x_intersects, y_intersects = getIntersects(array, len_intersects)
            for i in range(len_intersects):
                featureValues.append(x_intersects[i])
                featureValues.append(y_intersects[i])
            featureValues.append(label)
            allOutputs.append(featureValues)

            if len(header) == 0:
                header.extend(labels)

    header.extend(createHeader(len_intersects))
    header.append('label')
    print(header)
    for row in allOutputs:
        print(row)

    featureFile = open("extractedFeatures.csv", "w")
    featureFile.write("")
    featureFile.close()

    featureFile = open("extractedFeatures.csv", "a")
    featureFile.write(str.join(',', header))
    featureFile.write('\n')
    for row in allOutputs:
        featureFile.write(','.join(str(x) for x in row))
        featureFile.write('\n')
    featureFile.close()

def createHeader(len_intersects):
    labels = []
    for i in range(len_intersects):
            labels.append(f"num_x_intersects_{i}")
            labels.append(f"num_y_intersects_{i}")
    return labels

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