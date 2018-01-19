# File name: webserver.py

"""
Envia para um webserver no Raspberry Pi informações de status das vagas.
* parking_spaces: Um dicionário onde as chaves são as vagas e os valores são o status de cada vaga.
  (True: vazia, False: ocupada)
"""

from flask import Flask

# Um dicionário contendo vagas e situação das mesmas
parking_spaces = {'1': True, '2': False, '3': True}

app = Flask(__name__)


@app.route('/')
def index():
    return str(parking_spaces)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
