import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score, average_precision_score

def encoder(df):
    encoder = LabelEncoder()
    df['bairro'] = encoder.fit_transform(df['bairro'])
    return df

def train_test(df):
    df = encoder(df)
    df = shuffle(df)
    X = df.loc[:, 'area':'bairro']
    y = df.loc[:, 'y']
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.3, random_state = 42)

    return X_train, X_val, y_train, y_val


def random_forest(df):
    X_train, X_val, y_train, y_val = train_test(df)
    model = RandomForestClassifier(random_state = 42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)

    return model, y_pred, y_val

def evaluate_model(model_name, y_val, y_pred):
    aps = np.round(average_precision_score(y_val, y_pred), 4)
    roc = np.round(roc_auc_score(y_val, y_pred), 4)
    print('Temos para o modelo {} teve um APS igual a {}'.format(model_name, aps))
    print('Temos para o modelo {} teve uma ROC_CURVE igual a {}'.format(model_name, roc))
