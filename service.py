#!flask/bin/python

import re
import scraper_clubs
import scraper_regions
import scraper_teams
import scraper_players
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

####################################################################################
@app.route('/dopl/api/v1.0/<region_id>/<int:club_id>/<int:team_id>', methods=['GET'])
def get_players(region_id=None, club_id=0, team_id=0):

    if region_id is None:
        abort(400) 

    if len(region_id) > 8:
        abort(400)

    if not re.match('^[A-Z]*$', region_id):
        abort(400)
    
    region_url = scraper_regions.nuliga_get_region_url(region_id)
    
    if region_url == None:
        abort(404)


####################################################################################
@app.route('/dopl/api/v1.0/<region_id>/<int:club_id>', methods=['GET'])
def get_teams(region_id=None, club_id=0):

    if region_id is None:
        abort(400) 

    if len(region_id) > 8:
        abort(400)

    if not re.match('^[A-Z]*$', region_id):
        abort(400)
    
    region_url = scraper_regions.nuliga_get_region_url(region_id)
    
    if region_url == None:
        abort(404)

    teams = scraper_teams.nuliga_get_teams(region_url, club_id)
    
    if len(teams) == 0:
        abort(404)

    return jsonify({'teams': teams})

####################################################################################
@app.route('/dopl/api/v1.0/<region_id>', methods=['GET'])
def get_clubs(region_id=None):

    if region_id == None:
        abort(400) 

    if len(region_id) > 8:
        abort(400)

    if not re.match('^[A-Z]*$', region_id):
        abort(400)

    region_url = scraper_regions.nuliga_get_region_url(region_id)

    if region_url == None:
        abort(404)

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