# -*- coding: utf-8 -*-

"""
Read a temp file with the status of parking spaces and sent it data to an web server.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return open('../file_temp.txt', 'r').read()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
