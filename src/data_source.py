import pandas as pd
from sklearn.model_selection import train_test_split 
import os

class DataSource():

    def __init__(self):
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.path, 'data')       
        self.data_path = os.path.join(self.data_dir, 'imoveis_label.xlsx')
        self.train_path = os.path.join(self.data_dir, 'train.csv')
        self.test_path = os.path.join(self.data_dir, 'test.csv')

    def generate_test_data(self):
        df = pd.read_excel(self.data_path)
        train, test = train_test_split(df, test_size=0.33, random_state=42, shuffle=True)
        train.to_csv(self.train_path, sep=';', index=False)
        test.to_csv(self.test_path, sep=';', index=False)

    def read_data(self, train = True):
        '''
            Read data from data path

            params: train: boolean, specify if is a train or test data

            returns: pd.Dataframe with values and pd.Series with labels
        '''

        if train:
            df = pd.read_csv(self.train_path, delimiter=';')
            return df

        df = pd.read_csv(self.test_path, delimiter=';')

        return df