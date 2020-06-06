import os.path
from flask import Flask
import os
import json
import run_backend
import time


app = Flask(__name__)

def get_predictions():
    imoveis = []

    novos_imoveis_json = "novos_imoveis.json"
    if not os.path.exists(novos_imoveis_json):
        run_backend.update_db()

    last_update = os.path.getmtime(novos_imoveis_json) * 1e9

    if time.time_ns() - last_update > (720-3600-1e9):
        run_backend.update_db()

    with open ('novos_imoveis.json', 'r') as data_file:
        for line in data_file:
            line_json = json.loads(line)
            imoveis.append(line_json)

    predictions = []
    for imovel in imoveis:
        predictions.append()

    predictions = sorted(predictions, key = lambda x: x[2], reverse = True)[:30]

    predictions_formatted = []
    for e in predictions:
        predictions_formatted.append('<tr><th></th></tr>')

    return '\n'.join(predictions_formatted), last_update

@app.route('/')
def main_page():
    preds, last_update = get_predictions()
    return """
    <head><h1> Recomendador de Imóveis</h1></head>
    <body>
    Segudos desde a útlima atualização: {}
    <table>
        {}
    </table>
    </body>
    """.format((time.time_ns() - last_update) / 1e9,)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')