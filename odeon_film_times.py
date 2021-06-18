from bs4 import BeautifulSoup  # clean up the info
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict


chrome_browser = webdriver.Chrome('./chromedriver.exe') # Create a webdriver object
chrome_browser.get('https://www.odeon.co.uk/cinemas/sheffield/') # use the above to get a webpage
WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[3]/div/div/div[2]/div/div/button'))).click() # click on accept cookies
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

for day in odeon_days: # Iterate over the days picked above
    day.click()
    time.sleep(3)
    WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div[4]/div/div[2]/div/div[2]/label'))).click()

    html = chrome_browser.page_source
    soup = BeautifulSoup(html, 'html.parser') # Grab html

    odeon_day_pick = soup.find('ul', attrs={'class':'v-carousel__track glider-track'})

    odeon_film_item = soup.findAll('li', attrs={"class":"v-showtime-picker-film-list__item"}) # get all the film list items

    odeon_film_list = []
    for film_info in odeon_film_item:
        title = film_info.find('div', attrs={'class':'v-film-title'}).getText()
        try:
            length = film_info.find('div', attrs={'class':"v-detail v-film-runtime"}).getText()
        except AttributeError as err:
            length = 'Unknown'

        time_section = film_info.findAll('li', attrs={'class':'v-showtime-list__item'}) # find times section in the film item
        amount = len(time_section)
        if amount == 0:
             continue


        times_list = OrderedDict({})
        odeon_dict = OrderedDict({})
        day_film_times = []
        date = ''
        for film_time in time_section: # for loop to iterate over times
            day = film_time.find('time', attrs={'class':'v-showtime-list-button__detail-start-time'})
            date = day['datetime']
            x = day.getText()
            day_film_times.append(x)

        day_film_times.append(f'{amount} showings')
        times_list.update({date[0:10]: day_film_times})
        odeon_dict.update({'Title': title, 'Film Length': length})
        odeon_dict.update(times_list)

        with open('Film Time files/odeon_times.txt', mode='a') as new_file:
            for key, value in odeon_dict.items():
                try:
                    new_file.write('%s:%s\n' % (key, value))
                except UnicodeEncodeError as err:
                    print('dodgey film name char')
                    continue
        with open('Film Time files/odeon_times.txt', mode='a') as new_file:
            new_file.write('\n')


        odeon_film_list.append(odeon_dict)



chrome_browser.close()