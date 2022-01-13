from pprint import pprint
import requests

UPDATE = True

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

STATUS = {
    'active': '量产',
    'on hole': '暂停',
    'preview': '试产'
}
FAQ = 'FAQ'
DOWNLOAD_CENTER = '下载中心'
PRODUCT_DETAIL = '产品详情'
NEW_PRODUCT_INFO = '新品信息'
OTHER = '未分类'
EVALUATION_BOARD = '评估板'

PRODUCT = {
    'Integrated Circuits': 'https://www.trinamic.com/products/integrated-circuits/',
    'Modules': 'https://www.trinamic.com/products/modules/',
    'Motors & Encoders': 'https://www.trinamic.com/products/drives/',
    'PANdrive Smart Motors': 'https://www.trinamic.com/products/pandrive-smart-motors/',
    'Evaluation Kits': 'https://www.trinamic.com/support/eval-kits/'
}

PRODUCT_POST_CATEGORY = {
    'Integrated Circuits': PRODUCT_DETAIL,
    'Modules': PRODUCT_DETAIL,
    'Motors & Encoders': PRODUCT_DETAIL,
    'PANdrive Smart Motors': PRODUCT_DETAIL,
    'Evaluation Kits': EVALUATION_BOARD
}

TRINAMIC_ROOT = 'https://trinamic.com'
QINIU_DNS_NAME = 'https://tmc-item.chiplinkstech.com/'


def format_value(td):
    if td.find('svg'):
        return 'Yes'
    else:
        return td.text


def format_name(name):
    for i in ':;\\/- .*':
        name = name.replace(i, '_')
    return name


def format_data(sections):
    result = {'title': sections.pop(1)}
    for section in sections:
        x = section.find('h2')
        if x is None:
            continue
        else:
            result[x.text] = section

    return result


def format_url(url: str):
    if url is None:
        return url

    filename = url.split('/')[-1]
    return QINIU_DNS_NAME + filename


def request(url):
    for i in range(3):
        try:
            print("Try Connect Times: ", i + 1)
            response = requests.get(url, headers=HEADERS, timeout=500)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException:
            raise ConnectionError(url)
