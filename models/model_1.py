import pandas as pd 
import os
from utils import evaluate_model, random_forest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FILE_NAME =  [i for i in os.listdir(DATA_DIR) if i.endswith('.xlsx')][0]

df = pd.read_excel(os.path.join(DATA_DIR, FILE_NAME))
print(df.head())

model_rf, y_pred_rf, y_val_rf = random_forest(df)

print(evaluate_model('random_forest', y_val_rf, y_pred_rf))


