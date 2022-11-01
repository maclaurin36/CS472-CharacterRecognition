import json
import numpy as np
import pandas as pd


def createFlatCharObjectFromJson(myJson):
    myObject = json.loads(myJson)
    return FlatCharacterObject([], myObject['label'], myObject['dfString'])

class FlatCharacterObject:

    def __init__(self, array, label, json=None):
        if json:
            self.dfString = json
        else:
            self.dfString = pd.DataFrame(array).to_json()
        self.label = label

    def to_json(self):
        return json.dumps({"dfString":self.dfString, "label":self.label})

    def get_array(self):
        return np.array(pd.read_json(self.dfString))

def readFile(filePath):
    labelFile = open(filePath, "r")
    charJsons = labelFile.readlines()
    allCharObjects = []
    for charJson in charJsons:
        myCharObject = createFlatCharObjectFromJson(charJson)
        allCharObjects.append(myCharObject)
    return allCharObjects