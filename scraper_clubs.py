import re
import timeit
import urllib.request
import traceback
import selenium as se
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as SEX
from cachetools import cached, TTLCache

club_cache = TTLCache(maxsize=10, ttl=432000)

#########################################################################
def _find_clubs(url, button_text, clubs_found):

    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})

    driver = se.webdriver.Chrome(chrome_options=options)
    driver.get(url)

    try:
        elem = driver.find_element_by_link_text(button_text)
    except SEX.NoSuchElementException:
        driver.close()
        raise ValueError('Button not found')

    elem.click()
    clubs_dict = _parse_markup_for_clubs(driver.page_source, clubs_found)

    driver.quit()

#########################################################################
def _find_clubs_on_first_page(url, clubs_found):
    page = urllib.request.urlopen(url)
    return _parse_markup_for_clubs(page.read(), clubs_found)

#########################################################################
def _parse_markup_for_clubs(markup, clubs_found):
    soup = BeautifulSoup(markup, features="html.parser")

    clubsLinks = soup.find_all("a", href=re.compile("vereine/verein/v"))

    for clubLink in clubsLinks:
        url = clubLink.get("href")
        match = re.search("/v/(.+?)\.html", url)
        clubs_found.append(
            {
                'id': int(match.group(1)),
                'name': clubLink.string.strip()
            }
        )

#########################################################################
@cached(club_cache)
def nuliga_get_clubs(region_url, print_clubs_found = False):

    if not region_url:
        raise ValueError('Parameter region_url must not be empty.')
    if not isinstance(region_url, str):
        raise ValueError('Parameter region_url must be from type string.')

    url = urllib.parse.urljoin(region_url, 'liga/vereine.html')
    print(url)

    clubs_found = []
    pageNumberList = [2,3,4,5,6,7,8,9,10]

    _find_clubs_on_first_page(url, clubs_found)

    for pageNumber in pageNumberList:
        try:
            _find_clubs(url, str(pageNumber), clubs_found)
        except Exception:
            traceback.print_exc()
            break

    if print_clubs_found:
        print(clubs_found)        

    return clubs_found

#########################################################################
# print(timeit.timeit(lambda: nuliga_get_clubs('https://www.ooetv.at', False), number=1))
# print(timeit.timeit(lambda: nuliga_get_clubs('https://www.ooetv.at', False), number=1))
# print(timeit.timeit(lambda: nuliga_get_clubs('https://www.ooetv.at', True), number=1))