import re
import timeit
import urllib.request
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=1, ttl=432000)

#########################################################################
@cached(cache)
def nuliga_get_regions(print_regions_found = False):

    regions_found = []

    page = urllib.request.urlopen('https://www.oetv.at')
    soup = BeautifulSoup(page.read(), features="html.parser")

    region_dropdown = soup.find('li', id='navbar-region-dropdown')

    for region_link in region_dropdown.find_all('a'):
        url = region_link.get("href")

        if url == '#':
            continue

        if region_link.string == 'ÖTV':
            continue

        regions_found.append(
            {
                'name': region_link.string,
                'url': url
            }
        )

    if print_regions_found:
        print(regions_found)

    return regions_found

#########################################################################
# print(timeit.timeit(lambda: nuliga_get_regions(False), number=1))
# print(timeit.timeit(lambda: nuliga_get_regions(False), number=1))
# print(timeit.timeit(lambda: nuliga_get_regions(True), number=1))

