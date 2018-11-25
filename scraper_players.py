import re
import timeit
import scraper_regions
import urllib.request
from bs4 import BeautifulSoup
from operator import itemgetter
from cachetools import cached, TTLCache

player_cache = TTLCache(maxsize=500, ttl=80000)

#########################################################################
@cached(player_cache)
def nuliga_get_players(region_id, club_id, team_id, print_players_found = False):

    region_url = scraper_regions.nuliga_get_region_url(region_id)
    if region_id is None:
        return []

    url = region_url + '/liga/vereine/verein/mannschaften/mannschaft/m/' + str(team_id) + '.html'

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), features='html.parser')

    players_found = []
    table = soup.find('table', attrs={'class':'table table-striped table-condensed'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        players_found.append([ele for ele in cols if ele]) # Get rid of empty values

    sorted_players_found = []

    for player in sorted(players_found, key=itemgetter(0)):
        sorted_players_found.append(
            {
                'itn': float(player[1].replace(',', '.')),
                'name': player[2].strip()
        })

    if print_players_found:
        print(sorted_players_found)

    return sorted_players_found

#########################################################################
#print(timeit.timeit(lambda: nuliga_get_players(389515, False), number=1))
#print(timeit.timeit(lambda: nuliga_get_players(389515, False), number=1))
#print(timeit.timeit(lambda: nuliga_get_players(389515, True), number=1))
