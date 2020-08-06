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

final_movie_data = []
for c in current_sections:
    a_tag = c.select_one('dl > dt > a')
    movie_title = a_tag.text
    movie_code = a_tag['href'][28:]
    # print(movie_title, movie_code)

    movie_data = {
        'movie_title': movie_title,
        'movie_code': movie_code
    }
    final_movie_data.append(movie_data)
    # with open('./movies.csv', 'a', newline='', encoding='utf-8') as f:
    #     writer = csv.DictWriter(f, fieldnames=['movie_title', 'movie_code'])
    #     writer.writerow(movie_data)

# print(final_movie_data)

headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=33EKWGTUFQAF6; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NRTK=ag#50s_gr#1_ma#-2_si#0_en#0_sp#0; nx_ssl=2; NM_THUMB_PROMOTION_BLOCK=Y; nid_inf=-1470484697; NID_AUT=GEHt4vlqgpU+zUuB3g37WJPvh7HR486qysr4ilJRQMt6bX3VWe3NyUxQd7bSUiXy; NID_JKL=evEC0N0MfCmvMM/WeBrKwqMOKq/7An9C2aZC7wwkLCU=; BMR=s=1596682443781&r=https%3A%2F%2Fm.blog.naver.com%2Fmenbaldotcom%2F221039667984&r2=https%3A%2F%2Fwww.google.com%2F; NID_SES=AAABbj9I49rVosK1nSOE67GxjqvH8MDOQFh/KuU2appof/1eh5VGFiZfmHz+X+6xx/RgECKhRKBg5OY9tsLiq6jQx7CJ9Gg8sOKv3B3yaFQ/FmLmlMkVh+jHCSUFERaDexODnB/1LRsGIrrq/OwH7HEwh3OJfCH1kVTZiOCiP51xulXBSHAHmOJs4oOkDFI75NWF0BxyrKlm2FGS20HpPTPNJGWPXtRUtCdFVYhcFQ6OuPCZiYPMTYD5SGRbaM5rKufgAP02d/NPWk5XosKzkmd2dAPAMu8zWos64yqxK2hBIXKxC3Ab2CWICR6ksdvxWc9NxAPA01yXXyTr/VdL7oo0NkMwAavrwS8RDGHchHGvGUeVRAOzdVkj4gpWmo0dmKxqO4EJjGFSQuc6hBOyD09MV52dvKqjOGLtuQitWJeigMkCoUj2OAVzlrWI4tNULK4WIYgEv4l61IXFIxwR6jm2ciZtItru+Jg4rboD1QqJr1yY; csrf_token=1bb00211-47b6-4751-a946-0a7177529d7d',
}


for movie in final_movie_data:
    movie_code = movie['movie_code']
    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )
    response = requests.get(
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.select(
        'body > div > div > div.score_result > ul > li'

    )
    print(movie['movie_title'])
    for r in result:
        point = r.select_one('div.star_score > em').text
        review = r.select_one(
            'div.score_reple > p > span:nth-last-child(1)').text.strip()
        print(point, review)
    print('=============================')
