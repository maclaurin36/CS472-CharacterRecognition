from imghdr import tests
import numpy as np
import math

from FeatureProcessor import FeatureProcessor
from FeatureData import Feature, FeatureList

class DensityProcessor(FeatureProcessor):
    def __init__(self, _DIMENSION=1):
        self.DIMENSION = _DIMENSION
        # how many sections to measure density?
        # DIMENSION x DIMENSION - ex) 4 x 4 leads to 16 features
        return

    # returns percentage of cells that are 1s
    # Assumes 1s and 0s
    def getDensity(self, arr):
        sum = 0
        numRows, numCols = np.shape(arr)
        numCells = numRows * numCols
        for i in range(numRows):
            row = arr[i]
            sum += np.sum(row)
        return sum / numCells

    def addFeaturesToList(self, featureList, arr):
        if (not type(featureList) is FeatureList):
            print('List passed in is not the right type')
            return

        fullDensityVal = self.getDensity(arr)
        featureList.addFeature(Feature('Dens', fullDensityVal))

        if (self.DIMENSION > 1):
            self.addDensitiesForSubArrays(featureList, arr)
        

    def addDensitiesForSubArrays(self, featureList, arr):
        if (not type(featureList) is FeatureList):
            print('List passed in is not the right type')
            return
        numRows, numCols = np.shape(arr)
        for i in range(self.DIMENSION):
            for j in range(self.DIMENSION):
                label = f'Dens_{i}_{j}'

                # get start and stop indeces
                startRowIndex = math.floor(i / self.DIMENSION * numRows)
                endRowIndex = math.floor((i + 1) / self.DIMENSION * numRows)
                startColIndex = math.floor(j / self.DIMENSION * numCols)
                endColIndex = math.floor((j + 1) / self.DIMENSION * numCols)

                # get sub array
                subArray = arr[startRowIndex : endRowIndex,startColIndex : endColIndex]
                densityVal = self.getDensity(subArray)

                featureList.addFeature(Feature(label, densityVal))

testArray = np.array([
    [0,0,0,1,0,0,0],
    [0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
    [0,1,1,1,1,1,0],
])


testArraySmall = np.array([
    [0, 1],
    [1, 0],
])

# proc = DensityProcessor(2)
# density = proc.getDensity(testArray)
# proc.addFeaturesToList([], testArray)
# print(density)