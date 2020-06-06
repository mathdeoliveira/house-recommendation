import pandas as pd 
from sklearn.metrics import roc_auc_score, average_precision_score

class Metrics():
    def __init__(self):
        pass

    def calculate_classification(self, y_true, y_pred):
        '''
        Calculate the metrics from a regression problem

        params: y_true: numpy.ndarray or pandas.series
                y_pred: numpy.ndarray or pandas.series
        returns: dict with metrics
        '''

        roc = roc_auc_score(y_true, y_pred)
        aps = average_precision_score(y_true, y_pred)

        return {'roc_auc_score': roc,
                'average_precision_score': aps
                }