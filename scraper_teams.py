import re
import timeit
import urllib.request
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache

team_cache = TTLCache(maxsize=500, ttl=432000)

#########################################################################
@cached(team_cache)
def nuliga_get_teams(url, club_id, print_teams_found = False):

    team_url = url + "/liga/vereine/verein/mannschaften/v/" + str(club_id) + ".html"
    teams_found = []

    page = urllib.request.urlopen(team_url)
    soup = BeautifulSoup(page.read(), features="html.parser")

    team_links = soup.find_all("a", href=re.compile("liga/vereine/verein/mannschaften/mannschaft/m"))

    for team_link in team_links:
        url = team_link.get("href")
        match = re.search("/m/(.+?)\.html", url)
        teams_found.append(
            {
                'id': match.group(1),
                'name': team_link.string.strip()
            }
        )

    if print_teams_found:
        print(teams_found)

    return teams_found

#########################################################################
# print(timeit.timeit(lambda: nuliga_get_teams('https://www.ooetv.at', 40039, False), number=1))
# print(timeit.timeit(lambda: nuliga_get_teams('https://www.ooetv.at', 40039, False), number=1))
# print(timeit.timeit(lambda: nuliga_get_teams('https://www.ooetv.at', 40039, True), number=1))

# print(timeit.timeit(lambda: nuliga_get_teams('https://tennis.wien', 10002, True), number=1))
