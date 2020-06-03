import pandas as pd 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier


from preprocessing import PreProcessing
from data_source import DataSource
from metrics import Metrics

class Experiments(): 
    def __init__(self):
        self.tested_algorithms = {'decision_tree' : DecisionTreeClassifier(),
                                  'random_forest' : RandomForestClassifier(),
                                  'logistic_regression' : LogisticRegression(),
                                  'catboost' : CatBoostClassifier(),
                                  'lgbm' : LGBMClassifier()
                                 }

        self.models = None

    def train_model(self, X_train, y_train):
        '''
        Train the model with specified experiments

        params: X_train pd.Dataframe with train data
                y_train pd.Series with train labels

        return: dict with trained model
        '''

        for alg in self.tested_algorithms.keys():
            print('Treinando o modelo', alg)
            test = self.tested_algorithms[alg]
            print(test)
            test.fit(X_train, y_train)
            if self.models is None:
                self.models = {alg : test}
            else:
                self.models.update({alg : test})
            return self.models

    def run_experiment(self):
        '''
        Run specified experiments

        return: dict with metrics
        '''

        pre = PreProcessing()
        ds = DataSource()
        met = Metrics()
        print('Reading Data')
        train_df = ds.read_data(train=True)

        test_df, y_test = ds.read_data(train=False)
        y_test = y_test['y']
        print('Preprocessing train data')
        X_train, y_train = pre.preprocess(train_df, train=True)
        print('Preprocessing test data')
        X_test = pre.preprocess(test_df[pre.train_features], train=False)
        print('Training model')
        models = Experiments().train_model(X_train, y_train)
        print('Running metrics')
        for model in models.keys():
            print(model)
            y_pred = models[model].predict(X_test)
            print(met.calculate_classification(y_test, pd.Series(y_pred)))
            metrics = met.calculate_classification(y_test, pd.Series(y_pred))
            pd.DataFrame.from_dict(metrics, orient='index').to_csv('../output/'+model+'.csv')
        return metrics