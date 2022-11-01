from AllFeaturesProcessor import AllFeaturesProcessor
from TestMatrixGenerator import TestMatrixGenerator

import pandas as pd

testMatrixGenerator = TestMatrixGenerator()
testMatrices = testMatrixGenerator.getListOfTestMatrices()

allFeaturesProcessor = AllFeaturesProcessor()

rowLabels = []
colLabels = []

dataset = []

for i in range(len(testMatrices)):
    testMatrix = testMatrices[i]

    rowLabels.append(testMatrix.label)

    featureValues, featureLabels = allFeaturesProcessor.getAllDerivedFeaturesAndLabels(testMatrix.arr)

    if len(colLabels) < 1:
        colLabels = featureLabels

    dataset.append(featureValues)

tableData = pd.DataFrame(dataset, columns=colLabels, index=rowLabels)
print(tableData)




