# File name: webserver.py

"""
Envia para um webserver no Raspberry Pi informações de status das vagas.
* parking_spaces: Um dicionário onde as chaves são as vagas e os valores são o status de cada vaga.
  (True: vazia, False: ocupada)
"""

from flask import Flask
import main

app = Flask(__name__)


@app.route('/')
def index():
    return open('../file_temp.txt', 'r').read()


def start():
    """
    Starts the web server.
    :return: None
    """
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    start()

# app.run(debug=True, host='0.0.0.0')
