import math
import copy
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score


def read_data():
    pandas_dataframe = pd.read_csv("../FeatureExtraction/extractedFeatures.csv")
    numpy_array = np.array(pandas_dataframe)
    return pandas_dataframe, numpy_array

def bin_data(numpy_array):
    ret = numpy_array.astype('float64')
    for i in range(10):
        ret[:, 0][(ret[:, 0] >= (i * .1)) & (ret[:, 0] < ((i + 1) * .1))] = i
        ret[:, 1][(ret[:, 1] >= (i * .1)) & (ret[:, 1] < ((i + 1) * .1))] = i
        ret[:, 2][(ret[:, 2] >= (i * .1)) & (ret[:, 2] < ((i + 1) * .1))] = i
        ret[:, 3][(ret[:, 3] >= (i * .1)) & (ret[:, 3] < ((i + 1) * .1))] = i
        ret[:, 4][(ret[:, 4] >= (i * .1)) & (ret[:, 4] < ((i + 1) * .1))] = i
        ret[:, 5][(ret[:, 5] >= (i * .1)) & (ret[:, 5] < ((i + 1) * .1))] = i
        ret[:, 6][(ret[:, 6] >= (i * .1)) & (ret[:, 6] < ((i + 1) * .1))] = i
    return ret


if __name__ == "__main__":
    pandas_dataframe, numpy_array = read_data()
    datax = numpy_array[:,:-1]
    datay = numpy_array[:,-1:]
    newdata = bin_data(datax)

    initialAccruacys = []

    for i in range(15):
        clf = DecisionTreeClassifier()
        initialAccuracy = cross_val_score(clf, newdata, datay, cv=10)
        initialAccuracy = sum(initialAccuracy) / 10
        initialAccruacys.append(initialAccuracy)

    clf = DecisionTreeClassifier(random_state=0)
    accuracy = cross_val_score(clf, newdata, datay, cv=10)
    accuracy = sum(accuracy)/10

    print("initial accuracy")
    print(accuracy)

    clf = DecisionTreeClassifier(random_state=0, criterion='gini')
    accuracy = cross_val_score(clf, newdata, datay, cv=10)
    accuracy = sum(accuracy) / 10

    print("gini accuracy")
    print(accuracy)

    clf = DecisionTreeClassifier(random_state=0, criterion='entropy')
    accuracy = cross_val_score(clf, newdata, datay, cv=10)
    accuracy = sum(accuracy) / 10

    print("entropy accuracy")
    print(accuracy)

    clf = DecisionTreeClassifier(random_state=0, criterion='log_loss')
    accuracy = cross_val_score(clf, newdata, datay, cv=10)
    accuracy = sum(accuracy) / 10

    print("log_loss accuracy")
    print(accuracy)

    clf = DecisionTreeClassifier(random_state=0, criterion='gini', splitter='random')
    accuracy = cross_val_score(clf, newdata, datay, cv=10)
    accuracy = sum(accuracy) / 10

    print("gini & random accuracy")
    print(accuracy)


    clf = DecisionTreeClassifier(random_state=0, criterion='gini',class_weight='balanced')
    accuracy = cross_val_score(clf, newdata, datay, cv=10)
    accuracy = sum(accuracy) / 10

    print("gini & balanced accuracy")
    print(accuracy)


    reduced = False
    removed = []

    while(reduced == False):
        index = 0
        dif = math.inf
        for i in range(newdata.shape[1]):
            test = copy.deepcopy(newdata)
            test = np.delete(test, i, axis=1)
            clf = DecisionTreeClassifier(random_state=0, criterion='gini', class_weight='balanced')
            accuracy2 = cross_val_score(clf, test, datay, cv=10)
            accuracy2 = sum(accuracy2) / 10
            temp = accuracy-accuracy2
            if temp < dif:
                dif = temp
                index = i
        if dif < 0:
            newdata = np.delete(newdata, index, axis=1)
            accuracy = newdata-dif
            removed.append(index)
        elif dif <= .001:
            newdata = np.delete(newdata, index, axis=1)
            removed.append(index)
        else:
            reduced = True

    clf = DecisionTreeClassifier(random_state=0, criterion='gini', class_weight='balanced')
    accuracy = cross_val_score(clf, newdata, datay, cv=10)
    accuracy = sum(accuracy) / 10

    print("removed features")
    print(removed)
    print("final score")
    print(accuracy)

    finalAccuracys = []
    for i in range(15):
        clf = DecisionTreeClassifier(criterion='gini', class_weight='balanced')
        accuracy = cross_val_score(clf, newdata, datay, cv=10)
        accuracy = sum(accuracy) / 10
        finalAccuracys.append(accuracy)

    print("initial score")
    print(initialAccruacys)
    print("final score")
    print(finalAccuracys)