import numpy as np
import pandas as pd

from FeatureData import FeatureList
from FeatureProcessor import FeatureProcessor
from SymmetryProcessor import SymmetryProcessor
from DensityProcessor import DensityProcessor


# This class is used to take an array of 1s and 0s, representing a character, and output derived features for the learning model.
#
#
#
class AllFeaturesProcessor:

    # Initialize with the array representation of the character
    def __init__(self):
        self.processors = self.getProcessors()

    def getProcessors(self):
        return [
            SymmetryProcessor(),
            DensityProcessor(4),
        ]

    # For each processor, add it's derived values (could be more than one) to the feature list
    # Return the row of feature values and labels
    def getAllDerivedFeaturesAndLabels(self, arr):

        featureList = FeatureList()

        for i in range(len(self.processors)):
            processor = self.processors[i]
            if (not type(processor) is FeatureProcessor):
                print('bad processor type')
            processor.addFeaturesToList(featureList, arr)

        return featureList.getFeatureValuesAsArray(), featureList.getLabels()


