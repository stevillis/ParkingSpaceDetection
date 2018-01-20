# File name: webserver.py

"""
Envia para um webserver no Raspberry Pi informações de status das vagas.
* parking_spaces: Um dicionário onde as chaves são as vagas e os valores são o status de cada vaga.
  (True: vazia, False: ocupada)
"""

import threading
import time

from flask import Flask


def time_parking_change(t):
    print('{} starting...'.format(threading.currentThread().getName()))
    # Thread is stopped for t seconds
    time.sleep(t)
    print('{} exiting...'.format(threading.currentThread().getName()))


def start_thread(t):
    w = threading.Thread(name='Thread 2', target=time_parking_change, args=(t,))
    w.start()

app = Flask(__name__)


park = ''

@app.route('/')
def index():
    # start_thread(10)  # wait 10 seconds to send the parking_spaces to webserver
    return str(park)


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
