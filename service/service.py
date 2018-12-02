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
@app.route('/dopl/api/v1.0/regions/<region_id>/clubs/<int:club_id>/teams/<int:team_id>/players', methods=['GET'])
def get_players(region_id=None, club_id=0, team_id=0):

    if not region_is_valid:
        abort(400) 

    if request.args.get('mock') is None:
        players = scraper_players.nuliga_get_players(region_id, club_id, team_id)    
    else:
        players = [{"itn":5.5,"name":"Walther, Jean-Daniel"},{"itn":6.0,"name":"Wiesm\u00fcller, Manfred"}]

    if len(players) == 0:
        abort(404)

    return jsonify({'players': players})

####################################################################################
@app.route('/dopl/api/v1.0/regions/<region_id>/clubs/<int:club_id>/teams', methods=['GET'])
def get_teams(region_id=None, club_id=0):

    if not region_is_valid:
        abort(400) 
    
    if request.args.get('mock') is None:
        teams = scraper_teams.nuliga_get_teams(region_id, club_id)
    else:
        teams = [{"id":"407938","name":"Herren 45 1 (2er)"},{"id":"407939","name":"Herren 45 2 (2er)"}]
    
    if len(teams) == 0:
        abort(404)

    return jsonify({'teams': teams})

####################################################################################
@app.route('/dopl/api/v1.0/regions/<region_id>/clubs', methods=['GET'])
def get_clubs(region_id=None):

    if not region_is_valid:
        abort(400) 

    if request.args.get('mock') is None:
        clubs = scraper_clubs.nuliga_get_clubs(region_id)
    else:
        clubs = [{"id":40001,"name":"UTC Aigen"},{"id":40002,"name":"UTC Altenberg"}]
    
    if len(clubs) == 0:
        abort(404)

    return jsonify({'clubs': clubs})

####################################################################################
@app.route('/dopl/api/v1.0/regions', methods=['GET'])
def get_regions():

    if request.args.get('mock') is None:
        return jsonify({'regions': scraper_regions.nuliga_get_regions()}), 201
    else:
        return jsonify('regions', [{"id":"OOETV","url":"https://www.ooetv.at"},{"id":"NOETV","url":"https://www.noetv.at"}])

####################################################################################
if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')
