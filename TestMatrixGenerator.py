import math
import numpy as np

class TestMatrix:
    def __init__(self, _label, _arr):
        self.label = _label
        self.arr = _arr

    def __repr__(self):
        return self.label

class TestMatrixGenerator:
    def __init__(self):
        return

    def getYDecFromXDec(self, x):
        if x < 0 or x > 1:
            print('bad input')
            return 0
        
        val = .65 / ( math.pow((2 * x - 1), 2) + .5) - .3
        return val


    def createGaussianMatrix(self, dim):
        if dim < 1:
            print('bad')
            return []
        arr = np.zeros((dim, dim))

        numCols = len(arr[0])
        numRows = len(arr)

        for j in range(numCols):
            # col = arr[:,j]
            xVal = j / numCols
            yThresh = self.getYDecFromXDec(xVal)
            for i in range(numRows):
                if (numRows - i) < (yThresh * numRows):
                    arr[i][j] = 1

        return arr

    def createAllZeroMatrix(self, dim):
        return np.zeros((dim,dim + 5))

    def createAllOnesMatrix(self, dim):
        return np.ones((dim,dim + 3))

    # gives a matrix with left half 1s and right half 0s
    def createTotallyAssymetricalMatrix(self, dim):
        arr = np.zeros((dim,dim))
        numCols = dim
        numRows = dim
        for j in range(math.floor(numCols / 2)):
            for i in range(numRows):
                arr[i][j] = 1

        return arr

    def createCharacterOneMatrix(self):
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
        return ONE

    def getListOfTestMatrices(self):
        matrices = [
            TestMatrix("Gaus", self.createGaussianMatrix(100)),
            TestMatrix("Asym", self.createTotallyAssymetricalMatrix(100)),
            TestMatrix("Zeros", self.createAllZeroMatrix(100)),
            TestMatrix("Ones", self.createAllOnesMatrix(99)),
            TestMatrix("ONE", self.createCharacterOneMatrix()),
        ]
        return matrices