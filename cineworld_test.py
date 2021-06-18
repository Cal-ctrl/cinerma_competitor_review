from bs4 import BeautifulSoup  # clean up the info
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict
import datetime

# Cineworld times grab
today = datetime.date.today()
friday = str(today + datetime.timedelta((4 - today.weekday()) % 7)) + '&view-mode=list'
saturday = str(today + datetime.timedelta((5 - today.weekday()) % 7)) + '&view-mode=list'
sunday = str(today + datetime.timedelta((6 - today.weekday()) % 7)) + '&view-mode=list'

cine_days = [friday, saturday, sunday]


def get_soups(html_list):
    cine_soups = []
    for day in html_list:
        chrome_browser = webdriver.Chrome('./chromedriver.exe')  # Create a webdriver object
        chrome_browser.get('https://www.cineworld.co.uk/cinemas/sheffield/8079#/buy-tickets-by-cinema?in-cinema=8079&at=' + day)  # use the above to get a webpage
        time.sleep(3)
        html = chrome_browser.page_source
        soup = BeautifulSoup(html, 'html.parser')  # Grab html
        cine_soups.append(soup)
        chrome_browser.close()
    return cine_soups

soup_list = get_soups(cine_days)

def get_film_time(soup_list):
    cine_film_items = []
    for film_soup in soup_list:
        film_divs = film_soup.findAll('div', attrs={'class': 'row movie-row'})
        cine_film_items.append(film_divs)
    return cine_film_items

cine_films = get_film_time(soup_list)
print(len(cine_films))

with open('Film Time files/cineworld_times.txt', mode='a') as new_file:
    new_file.writelines(f'Cineworld Film Times for the weekend\n\n')


def cine_film_dict(film_items):
    fri = film_items[0]
    sat = film_items[1]
    sun = film_items[2]
    for film_info in fri:
        film_dict = OrderedDict({})
        title = film_info.find('h3', attrs={'class': 'qb-movie-name'}).getText()
        length = film_info.find('div', attrs={'class': 'qb-movie-info'}).getText()
        times = film_info.findAll('a', attrs={'href': '#'})
        film_times = []
        for f_time in times:
            if not f_time.getText():
                continue
            else:
                film_times.append(f_time.getText())
        film_times.append(f'{len(film_times)} showings')
        film_dict.update({'Title': title, 'Length': length[1:], 'Friday': film_times})
        for sat_film_info in sat:
            sat_find_title = sat_film_info.find('h3', attrs={'class': 'qb-movie-name'}).getText()
            if title == sat_find_title:
                sat_times = sat_film_info.findAll('a', attrs={'href': '#'})
                sat_film_times = []
                for sat_f_time in sat_times:
                    if not sat_f_time.getText():
                        continue
                    else:
                        sat_film_times.append(sat_f_time.getText())
                sat_film_times.append(f'{len(sat_film_times)} showings')
                film_dict.update({'Saturday': sat_film_times})
            else:
                continue
            for sun_film_info in sun:
                sun_find_title = sun_film_info.find('h3', attrs={'class': 'qb-movie-name'}).getText()
                if title == sun_find_title:
                    sun_times = sun_film_info.findAll('a', attrs={'href': '#'})
                    sun_film_times = []
                    for sun_f_time in sun_times:
                        if not sun_f_time.getText():
                            continue
                        else:
                            sun_film_times.append(sun_f_time.getText())
                    sun_film_times.append(f'{len(sun_film_times)} showings')
                    film_dict.update({'Sunday': sun_film_times})
                else:
                    continue
        with open('Film Time files/cineworld_times.txt', mode='a') as new_file:
            for key, value in film_dict.items():
                new_file.write('%s:%s\n' % (key, value))
            new_file.write('\n')
    return print('All done')

cine_film_dict(cine_films)






