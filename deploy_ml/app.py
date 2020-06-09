import sys
import os
import streamlit 
import pandas as pd
import pymysql
import time
from joblib import load
from preprocessing import PreProcessing

@st.cache()
def main():
    host = 'rds.amazonaws.com'
    port = 3306
    dbname = 'imoveis'
    user = 'admin'
    password = 'senha_nao_funciona_ta?'
    conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
    query = 'select * from imoveis_udi'
    df = pd.read_sql(query, con=conn)
    new_df = df.copy()

    streamlit.title('Recomendador de Imóveis')
    streamlit.write('Dados dos imóveis foram retirados por meio do web scraping e salvos no serviço de cloud da AWS.')

    streamlit.write('Para saber mais sobre o projeto, entre no GitHub para mais informações:')
    streamlit.markdown('[Clique aqui](https://github.com/mathdeoliveira/house-recommendation)')

    streamlit.subheader('Machine Learning em funcionamento')

    path = os.path.dirname(os.path.abspath(__file__))
    
    modelo = load(os.path.join(path, 'modelo.pkl'))

    new_df = modelo['preprocessing'].preprocess(new_df, train=False)
    y_pred = modelo['model'].predict_proba(new_df)[:, 1]
    df['Score'] = y_pred

    bar = streamlit.progress(0)
    for i in range(100):
        bar.progress(i + 1)
        if i == 15:
            streamlit.write('Conectando na AWS e recuperando dados')
        if i == 30:
            streamlit.write('Pre processamento dos dados para o algoritmo')
        if i == 50:
            streamlit.write('Iniciando previsão dos valores com o modelo CatBoostClassifier')   
        if i == 99:
            streamlit.table(df.sort_values(by = 'Score', ascending = False).head(30).reset_index(drop = True))
        time.sleep(0.1)

if __name__ == '__main__':
    main()