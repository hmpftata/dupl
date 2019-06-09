#!flask/bin/python

import re
import scraper_clubs
import scraper_regions
import scraper_teams
import scraper_players
from flask import Flask, request, abort
from flask_restplus import Resource, Api

app = Flask(__name__)

api = Api(app, version='1.0', title='Austria ITN API',
    description='An ITN API for austrian tennis players.',
)

ns = api.namespace('atitn', description='ITN operations')

####################################################################################
def region_is_valid(region_id):
    
    if region_id is None:
        return False

    if len(region_id) > 8:
        return False

    if not re.match('^[A-Z]*$', region_id):
        return False

####################################################################################
@ns.route('/regions/<region_id>/clubs/<int:club_id>/teams/<int:team_id>/players')
@ns.param('region_id', 'An region ID')
@ns.param('club_id', 'An club ID')
@ns.param('team_id', 'An team ID')
class Players(Resource):

    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid region_id')
    @ns.response(404, 'No players found for a specific region, club and team')
    def get(self, region_id=None, club_id=0, team_id=0):
        """Gets a list of players for a specific region, club and team."""

        if not region_is_valid:
            abort(400) 

        players = scraper_players.nuliga_get_players(region_id, club_id, team_id)    

        if len(players) == 0:
            abort(404)

        return {'players': players}

####################################################################################
@ns.route('/regions/<region_id>/clubs/<int:club_id>/teams')
@ns.param('region_id', 'An region ID')
@ns.param('club_id', 'An club ID')
class Team(Resource):

    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid region_id')
    @ns.response(404, 'No teams found for a specific region and club')
    def get(self, region_id=None, club_id=0):
        """Gets a list of teams for a specific club and region."""

        if not region_is_valid:
            abort(400) 
        
        teams = scraper_teams.nuliga_get_teams(region_id, club_id)
        
        if len(teams) == 0:
            abort(404)

        return {'teams': teams}

####################################################################################
@ns.route('/regions/<region_id>/clubs')
@ns.param('region_id', 'An region ID')
class Club(Resource):

    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid region_id')
    @ns.response(404, 'No clubs found for a specific region')
    def get(self, region_id=None):
        """Gets a list of clubs for a specific region."""

        if not region_is_valid:
            abort(400) 

        clubs = scraper_clubs.nuliga_get_clubs(region_id)
        
        if len(clubs) == 0:
            abort(404)

        return {'clubs': clubs}

####################################################################################
@ns.route('/regions')
class Regions(Resource):

    @ns.response(200, 'Success')
    @ns.response(201, 'Mock data returned')
    def get(self):
        """Gets a list of regions available for AT."""
        return {'regions': scraper_regions.nuliga_get_regions()}
        
####################################################################################
if __name__ == '__main__':
    #app.run(ssl_context='adhoc')
    #app.run(host='0.0.0.0', ssl_context='adhoc')
    app.run(host='0.0.0.0')
