from bs4 import BeautifulSoup  # clean up the info
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict


chrome_browser = webdriver.Chrome('./chromedriver.exe') # Create a webdriver object
# Vue Film Times Grab
chrome_browser.get('https://www.myvue.com/cinema/sheffield/whats-on') # use the above to get a webpage
WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/button[2]'))).click() # click on accept cookies
WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div/ul/li[8]/label'))).click() # click on "All Times"

time.sleep(3)
element_at_bottom_of_page = chrome_browser.find_element_by_xpath('/html/body/div[1]/footer/div[1]/section/ul/li[2]/section/div[2]/div/ul/li[1]/a') # elemnt at bottom of the page
chrome_browser.execute_script("arguments[0].scrollIntoView();", element_at_bottom_of_page) # Scroll

time.sleep(10)
html = chrome_browser.page_source
soup = BeautifulSoup(html, 'html.parser') # Grab html
film_name = soup.findAll('span', attrs={'rv-text':'item.title'}) # find all film titles, creates list.


names = []
for film in film_name: # iterate over list to get the names from element
    title = film.getText()
    names.append(title)

vue_film_item = soup.findAll('div', attrs={"class":"filmlist__item"}) # get all the film list items
vue_film_list = []
for film_info in vue_film_item:
    info = film_info.find('div', attrs={"class":"filmlist__info"})
    title = info.find('span', attrs={'rv-text':'item.title'}).getText()
    try:
        length = info.find('dd', attrs={'rv-text':"item.info_runningtime"}).getText()
    except AttributeError as err:
        length = 'Unknown'
    try:
        release = info.find('dd', attrs={'rv-text':"item.info_release"}).getText()
    except AttributeError as err:
        release = 'Unknown'

    time_section = film_info.findAll('time', attrs={'rv-datetime':'showing.date_time'}) # find times section in the film item

    times_list = OrderedDict({})
    for time in time_section: # for loop to iterate over time section grabbed above
        day_film_times = []
        day = time['datetime']
        for time in time_section:
            current_day = time['datetime'] # Possible want to see if this is Fri-Sun? midweek not needed?
            if day == current_day:
                x = time.getText()
                day_film_times.append(x)
            else:
                continue
        times_list.update({day: day_film_times}) # Add len of each times list as amount of shows
        amount_shows = len(day_film_times)
        day_film_times.append(f"{amount_shows} showings")


    vue_dict = OrderedDict({})
    vue_dict.update({'Title': title, 'Film Length': length, 'Release':release})
    vue_dict.update(times_list)
    with open('Film Time files/vue_times.txt', mode='a') as new_file:
        new_file.writelines('Vue Film Times\n\n')
        for key, value in vue_dict.items():
          new_file.write('%s:%s\n' % (key, value))

    vue_film_list.append(vue_dict)
chrome_browser.close()
