import category_encoders as ce 
import pandas as pd
from sklearn.preprocessing import StandardScaler

class PreProcessing():
    def __init__(self):
        self.feature_names = None
        self.std_scaler = None
        self.categoric_features = None
        self.numeric_features = None
        self.catb = None
        self.scaler = None
        self.train_features = None

    def preprocess(self, df, train = True):
        '''
        Process data for training model

        :param df: pandas Dataframe
               train: boolean
        :return processed pandas dataframe and pd.Series with target
        '''
        print('Creating dataframe for data manipulation')
        cons = pd.DataFrame({'column': df.columns,
                             'missing_perc': (df.isna().sum() / df.shape[0]) * 100,
                             'dtype': df.dtypes})
        print('Droping columns with missing values')
        cons = cons[cons['missing_perc'] == 0]
        print('Dropping column with id')
        cons = cons[cons['column'] != 'Id']
        print('Creating list with numeric features')
        numeric_features = list(cons[(cons['dtype'] == 'int64') | (cons['dtype'] == 'float') | (cons['dtype'] == 'bool')]['column'])
        print('Creating list with categorical features')
        categoric_features = list(cons[(cons['dtype'] == 'object')]['column'])
        self.categoric_features = categoric_features
        print('removing target')
        if train == True:
            numeric_features.remove('y')
        else:
            pass
        print(self.categoric_features)
        print('feature encoder')
        print('feature normalization and encoding')
        std_scaler = StandardScaler()
        if train == True:
            y = df['y']
            df = df.drop(columns = {'y'})
            self.numeric_features = numeric_features
            self.categoric_features = categoric_features
            self.feature_names = self.numeric_features + self.categoric_features
            self.scaler = std_scaler
            self.catb = ce.CatBoostEncoder(cols = self.categoric_features)
            df[self.numeric_features] = self.scaler.fit_transform(df[self.numeric_features])
            df[self.categoric_features] = self.catb.fit_transform(df[self.categoric_features], y=y)
            self.train_features = self.numeric_features + self.categoric_features
            return df[self.categoric_features + self.numeric_features], y
        else:
            df[self.numeric_features] = self.scaler.transform(df[self.numeric_features])
            df[self.categoric_features] = self.catb.transform(df[self.categoric_features])
            for column in df[self.categoric_features + self.numeric_features].columns:
                df[column] = df[column].fillna(df[column].mean())
            return df[self.categoric_features + self.numeric_features]