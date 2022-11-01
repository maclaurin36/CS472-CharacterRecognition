# Holds the label of the feature and its value
class Feature:
    def __init__(self, _label, _value):
        self.label = _label
        self.value = _value

# A list of all of the features. This object will be passed to the processors and the processors will add their features to this list
class FeatureList:
    def __init__(self):
        self.features = []

    def addFeature(self, feature):
        self.features.append(feature)

    def getLabels(self):
        labels = []

        for i in range(len(self.features)):
            feature = self.features[i]
            labels.append(feature.label)

        return labels

    def getFeatureValuesAsArray(self):
        data = []
        for i in range(len(self.features)):
            feature = self.features[i]
            data.append(feature.value)
        return data