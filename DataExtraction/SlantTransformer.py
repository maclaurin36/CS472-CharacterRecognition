import numpy as np
import math
import matplotlib.pyplot as plt

from FlatCharacterObject import *

def printMatrixOnGraph(matrices):
    colors = ['red','blue','orange','green','purple',]
    for matrixIndex in range(len(matrices)):
        matrix = matrices[matrixIndex]
        color = colors[matrixIndex % len(colors)]
        numRows, numCols = np.shape(matrix)
        for i in range(numRows):
            for j in range(numCols):
                if matrix[i][j] == 1:
                    plt.scatter(j, numRows - i, c=color, alpha=.1)
    plt.show()

ONE = np.array([
    [0,0,0,1,0,0,0],
    [0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,1,1,1,1,1,0],
])

class SlantTransformer:
    def __init__(self):
        return

    # @param slantVal represents how much to slant and which way.
    # The magnitude represents how much the width will grow (by a fraction of itself) .1 -> 1.1 times the original width, 1.0 -> 2 times the original width
    #
    # .1 will slant the char slightly to the right, 1.0 will slant the char a lot to the right
    # -.1 will slant slightly to the left, -1.0 will slant a lot to the left
    #
    def getSlantedMatrix(self, matrix, slantVal):
        numRows, numCols = np.shape(matrix)
        isSlantedRight = slantVal < 0
        offset = math.floor(numRows * abs(slantVal))

        newMatrix = np.zeros((numRows, numCols + offset))

        for i in range(numRows):
            startOffset = math.floor(i / numRows * offset)
            endOffset = offset - startOffset

            numLeftOffset = startOffset if isSlantedRight else endOffset
            numRightOffset = endOffset if isSlantedRight else startOffset

            # add left offset
            for j in range(numLeftOffset):
                newMatrix[i][j] = 0

            # add original row
            for j in range(numCols):
                newMatrix[i][numLeftOffset + j] = matrix[i][j]

            # add right offset
            for j in range(numRightOffset):
                newMatrix[i][numLeftOffset + numCols + j] = 0

        return newMatrix

slantTransformer = SlantTransformer()

oneSlantedRight = slantTransformer.getSlantedMatrix(ONE, 1)
oneSlantedLeft = slantTransformer.getSlantedMatrix(ONE, -1)
printMatrixOnGraph([ONE, oneSlantedRight, oneSlantedLeft])

# Test with actual data

localPath = 'C:\\Users\\Adam\\School\\CS472\\Group Project\\CS472-CharacterRecognition\\DataExtraction\\'
charMatrices = readFile(localPath + 'characters.txt')

dataIndex = 325

for bigChar in charMatrices[dataIndex : dataIndex + 5]:
    matrix = bigChar.get_array()
    matrixSlant = slantTransformer.getSlantedMatrix(matrix, .3)
    matrixSlantTwo = slantTransformer.getSlantedMatrix(matrix, -.3)
    printMatrixOnGraph([matrix, matrixSlant, matrixSlantTwo])










