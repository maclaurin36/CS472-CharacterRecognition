import math
import numpy as np

from FeatureProcessor import FeatureProcessor
from FeatureData import Feature, FeatureList

# Class used to calculate symmetry of an array
# Derived classes are for Horizontal and Vertical Symmetry
#
#
#
#
class SymmetryProcessor(FeatureProcessor):

    def __init__(self):
        return

    def getHorizontalSymmetry(self, arr):
        # some bounds checking
        numRows = len(arr)
        if numRows < 1:
            print('bad array getting symmetry')
            return 0
        numCols = len(arr[0])
        if numCols < 1:
            print('bad array getting symmetry')
            return 0

        numIterations = math.floor(numCols / 2)
        maxDifference = numRows
        totalComparisonRating = 0

        # column by column, compare number of 1s
        for i in range(numIterations):
            leftIndex = i
            leftColumn = arr[:,leftIndex]

            rightIndex = numCols - i - 1
            rightColumn = arr[:,rightIndex]

            leftVal = self.getNumberOfFilledCells(leftColumn)
            rightVal = self.getNumberOfFilledCells(rightColumn)

            # TODO - figure out best way to calculate symmetry
            comparisonRating = 1 - abs(leftVal - rightVal) / maxDifference
            totalComparisonRating += comparisonRating

        # Squaring it here to make the values a little more drastic. We can tweak this a bit as we figure out what are good symmetry values
        symmetryValue = math.pow(totalComparisonRating / numIterations, 2)

        return symmetryValue

    def getNumberOfFilledCells(self, arr):
        # right now this expects 1s or 0s. It probably won't work if we changed how we represented the matrices
        return sum(arr)

    def getTransposeArr(self, arr):
        return np.transpose(np.copy(arr))

    def getVerticalSymmetry(self, arr):
        arr_transpose = self.getTransposeArr(arr)
        return self.getHorizontalSymmetry(arr_transpose)


    # Derive the features from the array and add them to the feature list
    def addFeaturesToList(self, featureList, arr):
        if (not type(featureList) is FeatureList):
            print('List passed in is not the right type')
            return

        hSym = self.getHorizontalSymmetry(arr)
        vSym = self.getVerticalSymmetry(arr)

        horizSymFeature = Feature("H Sym", hSym)
        vertSymFeature = Feature("V Sym", vSym)

        featureList.addFeature(horizSymFeature)
        featureList.addFeature(vertSymFeature)


    