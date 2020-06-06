import pandas as pd 
from lightgbm import LGBMClassifier
from joblib import dump, load

from data_source import DataSource
from preprocessing import PreProcessing
from metrics import Metrics

class ModelTraining():
    def __init__(self):
        self.data = DataSource()
        self.preprocessing = None

    def model_training(self):
        pre = PreProcessing()
        print('Reading data')
        df = self.data.read_data(train = True)
        print('Starting training')
        X_train, y_train = pre.preprocess(df, train = True)
        print('Starting training model')
        model = LGBMClassifier()
        model.fit(X_train, y_train)
        model = {
            'model' : model,
            'preprocessing': pre,
            'columns': pre.feature_names
        }
        print(model)
        dump(model, '../output/modelo.pkl')
        return model