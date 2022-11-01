
from FeatureData import FeatureList

# Base class for all feature processors
# This isn't super because there's no abstract functions in python
# Not even saving lines of code - just to keep ideas organized.
class FeatureProcessor:
    def __init__(self):
        return

    # derived classes should implement an addFeaturesToList(FeatureList list, arr) function
    # array is the matrix representation of the character / image
    def addFeaturesToList(self, featureList, arr):
        print("Override me!")
