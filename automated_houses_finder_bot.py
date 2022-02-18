import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# program which aims to collect data from zillow webpage about houses in New York to rent, up to 3k$/month, with min. 1 bedroom
# collect the addresses, prices and links to offer, then filling special google forms with this data
# finnaly you can create a google sheet based on that filled up forms
# https://www.zillow.com/new-york-ny/rentals/1-_beds/?searchQueryState=%7B"pagination"%3A%7B%7D%2C"usersSearchTerm"%3A"New%20York%2C%20NY"%2C"mapBounds"%3A%7B"west"%3A-74.49191854882811%2C"east"%3A-73.46744345117186%2C"south"%3A40.374620443392125%2C"north"%3A41.01952192302355%7D%2C"regionSelection"%3A%5B%7B"regionId"%3A6181%2C"regionType"%3A6%7D%5D%2C"isMapVisible"%3Afalse%2C"filterState"%3A%7B"price"%3A%7B"min"%3A0%2C"max"%3A872627%7D%2C"mp"%3A%7B"min"%3A0%2C"max"%3A3000%7D%2C"beds"%3A%7B"min"%3A1%7D%2C"fsba"%3A%7B"value"%3Afalse%7D%2C"nc"%3A%7B"value"%3Afalse%7D%2C"fore"%3A%7B"value"%3Afalse%7D%2C"cmsn"%3A%7B"value"%3Afalse%7D%2C"fr"%3A%7B"value"%3Atrue%7D%2C"ah"%3A%7B"value"%3Atrue%7D%7D%2C"isListVisible"%3Atrue%7D

# -------Setup-------
google_form_adress = "https://docs.google.com/forms/d/e/1FAIpQLSdPspzwFK5dPBOtfOqG9vQvsXryYnssiCvqb7pyLb67qPafhw/viewform?usp=sf_link"
zillow_adress_with_filters = 'https://www.zillow.com/new-york-ny/rentals/1-_beds/?searchQueryState=%7B"usersSearchTerm"%3A"New%20York%2C%20NY"%2C"mapBounds"%3A%7B"west"%3A-76.02863119531249%2C"east"%3A-71.93073080468749%2C"south"%3A39.39559127782251%2C"north"%3A41.97514398991422%7D%2C"mapZoom"%3A8%2C"regionSelection"%3A%5B%7B"regionId"%3A6181%2C"regionType"%3A6%7D%5D%2C"isMapVisible"%3Afalse%2C"filterState"%3A%7B"price"%3A%7B"min"%3A0%2C"max"%3A872627%7D%2C"beds"%3A%7B"min"%3A1%7D%2C"fore"%3A%7B"value"%3Afalse%7D%2C"mp"%3A%7B"min"%3A0%2C"max"%3A3000%7D%2C"ah"%3A%7B"value"%3Atrue%7D%2C"nc"%3A%7B"value"%3Afalse%7D%2C"fr"%3A%7B"value"%3Atrue%7D%2C"cmsn"%3A%7B"value"%3Afalse%7D%2C"fsba"%3A%7B"value"%3Afalse%7D%7D%2C"isListVisible"%3Atrue%7D'
PRICES_LIST = []
LINKS_LIST = []
ADDRESSES_LIST = []

# -------Scraping-------
# accept_language and user_agent are needed to headers to get response, we can get it from http://myhttpheader.com
header = {
    "User-Agent": os.environ.get("user_agent"),
    "Accept-Language": os.environ.get("language"),
}

# i'm gettig data only from first page but if we want get data from more pages, its not problem all you need to do is
# for loop and add /{page_number}_p to URL
response = requests.get(zillow_adress_with_filters, headers=header)

web_content = response.text
soup = BeautifulSoup(web_content, 'html.parser')


offers = soup.find_all(name="div", class_="list-card-info")

for offer in offers:
    try:
        link_url = offer.find("a")["href"]
        if link_url[:5] == "https":
            LINKS_LIST.append(link_url)
        else:
            link_url = "https://www.zillow.com" + link_url
            LINKS_LIST.append(link_url)
        address = offer.find("address", class_="list-card-addr").text
        ADDRESSES_LIST.append(address)
        price = offer.find("div", class_="list-card-price").text
        PRICES_LIST.append(price)
    except:
        print("It's not an offer.")


# -------Filling forms-------
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())

for i in range(len(PRICES_LIST)):
    driver.get(google_form_adress)

    adress_input = driver.find_element_by_css_selector('input[aria-labelledby="i1"]')
    adress_input.send_keys(ADDRESSES_LIST[i])

    price_input = driver.find_element_by_css_selector('input[aria-labelledby="i5"]')
    price_input.send_keys(PRICES_LIST[i])

    link_input = driver.find_element_by_css_selector('input[aria-labelledby="i9"]')
    link_input.send_keys(LINKS_LIST[i])

    driver.find_element_by_css_selector('span[class="appsMaterialWizButtonPaperbuttonLabel quantumWizButtonPaperbuttonLabel exportLabel"]').click()
    time.sleep(2)
