import pandas as pd 
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold

from preprocessing import PreProcessing
from data_source import DataSource
from metrics import Metrics

class Experiments(): 
    def __init__(self):
        self.tested_algorithms = {'decision_tree' : DecisionTreeClassifier(),
                                  'random_forest' : RandomForestClassifier(),
                                  'logistic_regression' : LogisticRegression(),
                                  'catboost' : CatBoostClassifier(),
                                  'lgbm' : LGBMClassifier(),
                                  'xgboost': XGBClassifier()
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
            steps = [('over', SMOTE()), ('model', test)]
            pipeline = Pipeline(steps=steps)
            pipeline.fit(X_train, y_train)
            print('Cross val score using RepeatedStratifiedKFold')
            cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=5, random_state=42)
            scores = cross_val_score(pipeline, X_train, y_train, scoring='roc_auc', cv=cv, n_jobs=-1)
            print(np.mean(scores))
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
        test_df = ds.read_data(train=False)
        y_test = test_df['y']
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
            print(met.calculate_classification(model, y_test, pd.Series(y_pred)))
            metrics = met.calculate_classification(model, y_test, pd.Series(y_pred))
            pd.DataFrame.from_dict(metrics, orient='index').to_csv('../output/'+model+'.csv')
        return metrics