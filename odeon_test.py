from bs4 import BeautifulSoup  # clean up the info
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict


chrome_browser = webdriver.Chrome('./chromedriver.exe') # Create a webdriver object
chrome_browser.get('https://www.odeon.co.uk/cinemas/sheffield/') # use the above to get a webpage
WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div/div[2]/div/div/button'))).click() # click on accept cookies
time.sleep(3)
WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div[4]/div/div[2]/div/div[2]/label/div[1]'))).click() # click on "All films"
time.sleep(3)
try:
    WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/svg/g/path'))).click() # close banner
except:
    pass
time.sleep(3)

odeon_fri = chrome_browser.find_elements_by_xpath('//*/button[contains(.,"Fri")]')
odeon_sat = chrome_browser.find_elements_by_xpath('//*/button[contains(.,"Sat")]')
odeon_sun = chrome_browser.find_elements_by_xpath('//*/button[contains(.,"Sun")]')

odeon_days = [odeon_fri[0], odeon_sat[0], odeon_sun[0]]

WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div[4]/div/div[2]/div/div[1]/div/div/button[2]'))).click() # Click on slider to the right

with open('Film Time files/odeon_times.txt', mode='a') as new_file:
    new_file.write(f'Odeon Film times\n\n')


def write_times(film_ord_dict):
    with open('Film Time files/odeon_times.txt', mode='a') as new_file:
        for key, value in film_ord_dict.items():
            try:
                new_file.write('%s:%s\n' % (key, value))
            except UnicodeEncodeError as err:
                print('dodgey film name char')
                continue
        new_file.write('\n')

odeon_soups = []
for day in odeon_days: # Iterate over the days picked above
    day.click()
    time.sleep(3)
    WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div[4]/div/div[2]/div/div[2]/label'))).click()

    html = chrome_browser.page_source
    soup = BeautifulSoup(html, 'html.parser') # Grab html
    odeon_soups.append(soup)

def film_grab(soup_list):
    film_item_list = []
    for soup in soup_list:
        x = soup.findAll('li',attrs={"class": "v-showtime-picker-film-list__item"}) # get all the film list items
        film_item_list.append(x)
    return film_item_list

film_soup_list = film_grab(odeon_soups)

def creat_film_dict(film_items):
    film_dict = OrderedDict({})
    fri = film_items[0]
    sat = film_items[1]
    sun = film_items[2]
    for film_info in fri:
        title = film_info.find('div', attrs={'class': 'v-film-title'}).getText()
        try:
            length = film_info.find('div', attrs={'class':"v-detail v-film-runtime"}).getText()
        except AttributeError as err:
            length = 'Unknown'
        time_section = film_info.findAll('li',
                                     attrs={'class': 'v-showtime-list__item'})  # find times section in the film item
        amount = len(time_section)
        if amount == 0:
             continue

        film_dict.update({'Title':title})
        film_dict.update({'Running time':length[7:]})
        film_dict.update(get_times(time_section))
        for sat_film_info in sat:
            find_title = sat_film_info.find('div', attrs={'class': 'v-film-title'}).getText()
            if title == find_title:
                sat_time_section = sat_film_info.findAll('li',
                                                 attrs={'class': 'v-showtime-list__item'})
                film_dict.update(get_times(sat_time_section))
            for sun_film_info in sun:
                sun_find_title = sun_film_info.find('div', attrs={'class': 'v-film-title'}).getText()
                if title == sun_find_title:
                    sun_time_section = sun_film_info.findAll('li',
                                                 attrs={'class': 'v-showtime-list__item'})
                    film_dict.update(get_times(sun_time_section))
                else:
                    continue
            else:
                continue
        write_times(film_dict)


def get_times(time_items):
    time_dict_item = OrderedDict({})
    day_times = []
    for film_time in time_items:  # for loop to iterate over times
        day = film_time.find('time', attrs={'class':'v-showtime-list-button__detail-start-time'})
        date = day['datetime']
        x = day.getText()
        day_times.append(x)
    day_times.append(f'{len(day_times)} showings')
    time_dict_item.update({date[0:10]:day_times})
    return time_dict_item

creat_film_dict(film_soup_list)

chrome_browser.close()