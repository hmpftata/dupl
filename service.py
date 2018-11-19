#!flask/bin/python

import scraper_clubs as scc
from flask import Flask, jsonify

app = Flask(__name__)
clubs = scc.nuliga_get_clubs()

@app.route('/dopl/api/v1.0/clubs', methods=['GET'])
def get_clubs():
    return jsonify({'clubs': clubs})


if __name__ == '__main__':
    app.run(debug=True)