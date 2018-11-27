#!flask/bin/python

import re
import scraper_clubs
import scraper_regions
import scraper_teams
import scraper_players
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

####################################################################################
def region_is_valid(region_id):
	
    if region_id is None:
        return False

    if len(region_id) > 8:
        return False

    if not re.match('^[A-Z]*$', region_id):
        return False

####################################################################################
@app.route('/dopl/api/v1.0/<region_id>/<int:club_id>/<int:team_id>', methods=['GET'])
def get_players(region_id=None, club_id=0, team_id=0):

    if not region_is_valid:
        abort(400) 

    players = scraper_players.nuliga_get_players(region_id, club_id, team_id)    

    if len(players) == 0:
        abort(404)

    return jsonify({'players': players})

####################################################################################
@app.route('/dopl/api/v1.0/<region_id>/<int:club_id>', methods=['GET'])
def get_teams(region_id=None, club_id=0):

    if not region_is_valid:
        abort(400) 
    
    teams = scraper_teams.nuliga_get_teams(region_id, club_id)
    
    if len(teams) == 0:
        abort(404)

    return jsonify({'teams': teams})

####################################################################################
@app.route('/dopl/api/v1.0/<region_id>', methods=['GET'])
def get_clubs(region_id=None):

    if not region_is_valid:
        abort(400) 

    clubs = scraper_clubs.nuliga_get_clubs(region_id)
    
    if len(clubs) == 0:
        abort(404)

    return jsonify({'clubs': clubs})

####################################################################################
@app.route('/dopl/api/v1.0/regions', methods=['GET'])
def get_regions():
    return jsonify({'regions': scraper_regions.nuliga_get_regions()}), 201

####################################################################################
if __name__ == '__main__':
    app.run(debug=True)
