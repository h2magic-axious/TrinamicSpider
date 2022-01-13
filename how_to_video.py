import json

import requests
from bs4 import BeautifulSoup

ROOT_URL = "https://www.trinamic.com"
URL = f"{ROOT_URL}/support/how-to/"
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_gcl_au=1.1.1761685525.1587892701; _ga=GA1.2.246419009.1587892704; _gid=GA1.2.951589391.1587892704',
    'Host': 'www.trinamic.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
}

html = requests.get(URL, headers=HEADERS).text
soup = BeautifulSoup(html, 'lxml')

with open('video.json', 'w', encoding='utf-8') as f:
    result = {}
    divs = soup.find_all(class_="col-sm-12")[:-1]
    for div in divs:
        print(div)
        video_url = div.find('a')['href']
        video_image = f'{ROOT_URL}{div.find(class_="teaser-image").find("img")["src"]}'

        teaser = div.find(class_='teaser-wrapper')
        video_title = teaser.find(class_='teaser-header').text.strip()
        video_except = teaser.find(class_='teaser-body').text.strip()

        result[video_title] = {
            'url': video_url,
            'img': video_image,
            'except': video_except
        }

    json.dump(result, f)
