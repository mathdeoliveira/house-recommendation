import pandas as pd 
from catboost import CatBoostClassifier
from joblib import dump, load
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

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
        model = CatBoostClassifier()
        steps = [('over', SMOTE()), ('model', CatBoostClassifier())]
        pipeline = Pipeline(steps=steps)
        pipeline.fit(X_train, y_train)
        modelo = pipeline['model']
        model = {
            'model' : modelo,
            'preprocessing': pre,
            'columns': pre.feature_names
        }
        print(model)
        dump(model, '../output/modelo.pkl')
        return model