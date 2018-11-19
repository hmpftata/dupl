import re
import scraper as sc
import urllib.request
from bs4 import BeautifulSoup

#########################################################################
def nuliga_get_teams(club_id, print_teams_found = False):

    if not club_id:
        raise ValueError("Parameter club_id must not be empty.")
    if not isinstance(club_id, int):
        raise ValueError("Parameter club_id must be from type int.")

    url = "https://www.ooetv.at/liga/vereine/verein/mannschaften/v/" + str(club_id) + ".html"
    teams_found = []

    page = urllib.request.urlopen(url)
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
# nuliga_get_teams(40039, True)
