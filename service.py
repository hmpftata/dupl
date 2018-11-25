#!flask/bin/python

import scraper_clubs
import scraper_regions
import re
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

####################################################################################
@app.route('/dopl/api/v1.0/<region_id>/clubs', methods=['GET'])
def get_clubs(region_id='OÖTV'):
    
    if len(region_id) > 8:
        abort(400)

    if not re.match('^[A-Z]*$', region_id):
        abort(400)

    region_url = scraper_regions.nuliga_get_region_url(region_id)
    clubs = scraper_clubs.nuliga_get_clubs(region_url)
    
    if len(clubs) == 0:
        abort(404)

    return jsonify({'clubs': clubs})

####################################################################################
@app.route('/dopl/api/v1.0/regions', methods=['GET'])
def get_regions():
    return jsonify({'regions': scraper_regions.nuliga_get_regions()}), 201

if __name__ == '__main__':
    app.run(debug=True)