#!flask/bin/python

import re
import scraper_clubs
import scraper_regions
import scraper_teams
import scraper_players
from flask import Flask, Blueprint, request, abort
from flask_restplus import Resource, Api, fields
from marshmallow import Schema, fields as ma_fields, post_load
from functools import wraps
from cachetools import cached, TTLCache

app = Flask(__name__)

authorizations = {
    'apikey': {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    }
}

api = Api(app, authorizations=authorizations, version='1.0', title='Austria ITN API',
    description='An ITN API for austrian tennis players.',
)

ns = api.namespace('atitn', description='ITN operations')

token_cache = TTLCache(maxsize=1, ttl=432000)

####################################################################################
@cached(token_cache)
def token_read():
    
    token = ''
    
    with open('token.txt', 'r') as f:
        token = f.readline()
    
    token = token.rstrip('\n')
    token = token.strip()

    print('token found: ', token)

    return token

####################################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if token != token_read():
            return {'messaage' : 'Invalid token.'}, 401

        return f(*args, **kwargs)

    return decorated

####################################################################################
def region_is_valid(region_id):
    
    if region_id is None:
        return False

    if len(region_id) > 8:
        return False

    if not re.match('^[A-Z]*$', region_id):
        return False

####################################################################################
@api.route('/regions/<region_id>/clubs/<int:club_id>/teams/<int:team_id>/players')
@api.param('region_id', 'The ID of the players region.')
@api.param('club_id', 'The ID of the players club.')
@api.param('team_id', 'The ID of the players team.')
class Players(Resource):

    @api.response(200, 'Success')
    @api.response(400, 'Invalid region_id')
    @api.response(404, 'No players found for a specific region, club and team')
    @api.doc(security='apikey')
    @token_required
    def get(self, region_id=None, club_id=0, team_id=0):
        """Gets a list of players for a specific region, club and team."""

        if not region_is_valid:
            abort(400) 

        players = scraper_players.nuliga_get_players(region_id, club_id, team_id)    

        if len(players) == 0:
            abort(404)

        return {'players': players}

####################################################################################
@api.route('/regions/<region_id>/clubs/<int:club_id>/teams')
@api.param('region_id', 'The ID of the players region.')
@api.param('club_id', 'The ID of the players club.')
class Team(Resource):

    @api.response(200, 'Success')
    @api.response(400, 'Invalid region_id')
    @api.response(404, 'No teams found for a specific region and club')
    @api.doc(security='apikey')
    @token_required
    def get(self, region_id=None, club_id=0):
        """Gets a list of teams for a specific club and region."""

        if not region_is_valid:
            abort(400) 
        
        teams = scraper_teams.nuliga_get_teams(region_id, club_id)
        
        if len(teams) == 0:
            abort(404)

        return {'teams': teams}

####################################################################################
@api.route('/regions/<region_id>/clubs')
@api.param('region_id', 'The ID of the players region.')
class Club(Resource):

    @api.response(200, 'Success')
    @api.response(400, 'Invalid region_id')
    @api.response(404, 'No clubs found for a specific region')
    @api.doc(security='apikey')
    @token_required
    def get(self, region_id=None):
        """Gets a list of clubs for a specific region."""

        if not region_is_valid:
            abort(400) 

        clubs = scraper_clubs.nuliga_get_clubs(region_id)
        
        if len(clubs) == 0:
            abort(404)

        return {'clubs': clubs}

####################################################################################
@api.route('/regions')
class Regions(Resource):

    @api.response(200, 'Success')
    @api.doc(security='apikey')
    @token_required
    def get(self):
        """Gets a list of regions available for AT."""
        return {'regions': scraper_regions.nuliga_get_regions()}
        
####################################################################################
if __name__ == '__main__':
    #app.run()
    #app.run(ssl_context='adhoc')
    #app.run(host='0.0.0.0', ssl_context='adhoc')
    app.run(host='0.0.0.0')
