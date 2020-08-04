import requests
import csv
from bs4 import BeautifulSoup, NavigableString, Tag

base_url = f'https://movie.naver.com/movie/running/current.nhn'

response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# print(soup)

current_sections = soup.select(
    'div[id=container] > div[id=content] > div[class=article] > div[class=obj_section] > div[class=lst_wrap] > ul[class=lst_detail_t1] > li'
)

for c in current_sections:
    a_tag = c.select_one('dl > dt > a')
    movie_title = a_tag.text
    movie_code = a_tag['href'][28:]
    # print(movie_title, movie_code)

    movie_data = {
        'movie_title': movie_title,
        'movie_code': movie_code
    }

    with open('./movies.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=['movie_title', 'movie_code'])
        writer.writerow(movie_data)
