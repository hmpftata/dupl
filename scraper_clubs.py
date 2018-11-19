import re
import selenium as se
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as SEX

#########################################################################
def _find_clubs(url, button_text):

    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    
    driver = se.webdriver.Chrome(chrome_options=options)
    driver.get(url)

    try:
        elem = driver.find_element_by_link_text(button_text)
    except SEX.NoSuchElementException:
        driver.close()
        driver.quit()
        raise ValueError("Element ", button_text, " not found.")
        return

    elem.click()
    
    clubs_dict = _parse_markup_for_clubs(driver.page_source)

    driver.quit()

    return clubs_dict

#########################################################################
def _parse_markup_for_clubs(markup):
    soup = BeautifulSoup(markup, features="html.parser")

    clubsLinks = soup.find_all("a", href=re.compile("vereine/verein/v"))

    clubs_found = []

    for clubLink in clubsLinks:
        url = clubLink.get("href")
        match = re.search("/v/(.+?)\.html", url)
        clubs_found.append(
            { 
                'id': int(match.group(1)),
                'name': clubLink.string.strip()
            }
        )

    return clubs_found

#########################################################################
def nuliga_get_clubs(print_clubs_found = False):

    url = "https://www.ooetv.at/liga/vereine.html"

    clubs_found = []
    pageNumberList = [1,2,3,4,5,6,7,8,9,10]

    for pageNumber in pageNumberList:
        try:
            clubs_found.append(_find_clubs(url, str(pageNumber)))
        except:
            break

    if print_clubs_found:
        print(clubs_found)        

    return clubs_found

#########################################################################
nuliga_get_clubs(True)