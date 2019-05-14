import bs4
import requests


def get_site_code(link):
    return requests.get(link).text


def get_text(site):
    site = bs4.BeautifulSoup(site, 'html.parser')
    try:
        text = site.find_all('div', class_='lyrics')[0].get_text()
    except Exception:
        return ''
    return text


def get_all_links(season):
    site = bs4.BeautifulSoup(get_site_code(season), 'html.parser')
    links = site.find_all('a', class_="u-display_block")
    links = list(map(lambda x: x['href'], links))
    return links


seasons = ['https://genius.com/albums/Game-of-thrones/Season-1-scripts',
           'https://genius.com/albums/Game-of-thrones/Season-2-scripts',
           'https://genius.com/albums/Game-of-thrones/Season-3-scripts',
           'https://genius.com/albums/Game-of-thrones/Season-4-scripts',
           'https://genius.com/albums/Game-of-thrones/Season-5-scripts',
           'https://genius.com/albums/Game-of-thrones/Season-6-scripts',
           'https://genius.com/albums/Game-of-thrones/Season-7-scripts',
           'https://genius.com/albums/Game-of-thrones/Season-8-scripts'
           ]


all_links = []
for season in seasons:
    all_links += get_all_links(season)


for i in range(len(all_links)):
    print('Progress {}%'.format((i+1) * 100 / len(all_links)))
    with open('scripts/episode{}.txt'.format(i + 1), 'w') as script:
        script.write(get_text(get_site_code(all_links[i])))
