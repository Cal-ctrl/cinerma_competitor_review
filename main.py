import requests  # get url info
from bs4 import BeautifulSoup  # clean up the info
import pprint

res1 = requests.get('https://news.ycombinator.com/')
soup1 = BeautifulSoup(res1.text, 'html.parser')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup1.select('.storylink') + soup2.select('.storylink')  # selector allows us to grap a CSS selector
subtext = soup1.select('.subtext') + soup2.select('.subtext')


def sort_stroies_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['score'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'score': points})
    return sort_stroies_by_votes(hn)


print.pprint(create_custom_hn(links, subtext))
