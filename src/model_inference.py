import pandas as pd 
from joblib import dump, load

from model_training import ModelTraining
from metrics import Metrics
from preprocessing import PreProcessing
from data_source import DataSource
from metrics import Metrics

class ModelInference():
    def __init__(self):
        self.modelo = None

    def predict(self):
        '''
        Predict values using model trained
        return: pandas Series with predicted values
        '''

        print('Loading model')
        self.modelo = load('../output/modelo.pkl')
        print('Loading data')
        test_df = DataSource().read_data(train=False)
        print('Preprocessing Data')
        X_test = self.modelo['preprocessing'].preprocess(test_df, train=False)
        print(X_test.isna().sum())
        print('Predicting')
        y_pred = self.modelo['model'].predict(X_test)
        print('Evaluating model in test data')
        y_true = test_df['y']
        model_name = 'CatBoost'
        print(Metrics().calculate_classification(model_name, y_true, y_pred))
        print('Saving file')
        pd.DataFrame(y_pred).to_csv('../output/predito.csv')
        return y_pred