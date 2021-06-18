from bs4 import BeautifulSoup  # clean up the info
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict
import datetime


chrome_browser = webdriver.Chrome('./chromedriver.exe') # Create a webdriver object
# Cineworld times grab
today = datetime.date.today()
friday = str(today + datetime.timedelta((4-today.weekday()) % 7)) + '&view-mode=list'
saturday = str(today + datetime.timedelta((5-today.weekday()) % 7)) + '&view-mode=list'
sunday = str(today + datetime.timedelta((6-today.weekday()) % 7)) + '&view-mode=list'

def cine_friday(html):
    cine_film_times = []
    chrome_browser.get('https://www.cineworld.co.uk/cinemas/sheffield/8079#/buy-tickets-by-cinema?in-cinema=8079&at='+html) # use the above to get a webpage
    time.sleep(3)
    html = chrome_browser.page_source
    soup = BeautifulSoup(html, 'html.parser') # Grab html

    film_divs = soup.findAll('div', attrs={'class':'row movie-row'}) # find all film objects, creates list. Needs work
    for film in film_divs:
        film_dict = OrderedDict({})
        title = film.find('h3', attrs={'class':'qb-movie-name'}).getText()
        length = film.find('div', attrs={'class':'qb-movie-info'}).getText()
        times = film.findAll('a', attrs={'href':'#'})
        film_times = []
        for f_time in times:
            if not f_time.getText():
                continue
            else:
                film_times.append(f_time.getText())
        film_times.append(f'{len(film_times)} showings')
        film_dict.update({'Title':title, 'Length':length, 'Times':film_times})
        cine_film_times.append(film_dict)
    return cine_film_times


def print_days(film_dict_list, day):
    with open('Film Time files/cineworld_times.txt', mode='a') as new_file:
        new_file.writelines(f'Cineworld Film Times for {day}\n')
        for film in film_dict_list:
            for key, value in film.items():
                new_file.write('%s:%s\n' % (key, value))
        new_file.write('\n')
    return print('All done')


print_days(cine_friday(friday), 'Friday')
print_days(cine_friday(saturday), 'Saturday')
print_days(cine_friday(sunday), 'Sunday')



chrome_browser.close()




