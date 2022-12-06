import pandas as pd
import numpy as np

def read_data():
    pandas_dataframe = pd.read_csv("../FeatureExtraction/extractedFeatures.csv")
    numpy_array = np.array(pandas_dataframe)
    return pandas_dataframe, numpy_array

if __name__ == "__main__":
    pandas_dataframe, numpy_array = read_data()
    print(pandas_dataframe)
    print(numpy_array)
