import json

import requests
from bs4 import BeautifulSoup

from Reference import PRODUCT, format_name, TRINAMIC_ROOT, HEADERS, UPDATE, PRODUCT_POST_CATEGORY
from Memory import TrinamicMemory


class MainPage:
    def __init__(self):
        self.dns_name = TRINAMIC_ROOT

    def from_tr_get_element(self, tr: BeautifulSoup):
        tmp = tr.find('td')
        return tmp.text, self.dns_name + tmp.find('a')['href']

    def category_and_item(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(url)

        soup = BeautifulSoup(response.content, 'lxml')
        categories = (h2.text for h2 in soup.find_all('h2')[1:])
        body = soup.find_all('tbody')
        return {
            category: [self.from_tr_get_element(tr) for tr in by.find_all('tr')] for category, by in
            zip(categories, body)
        }

    def iter(self):
        for product, url in PRODUCT.items():
            categories = self.category_and_item(url)

            for category in categories:
                for model, url in categories[category]:
                    yield product, PRODUCT_POST_CATEGORY[product], category, model.strip(), url.strip()


def main():
    tm = TrinamicMemory()
    mp = MainPage()

    result = dict()
    p_c_m = []

    for product, post_category, category, model, url in mp.iter():
        category_dir = tm.category(True, format_name(product), format_name(category))
        model_html = category_dir.joinpath(model + '.html')

        p_c_m.append((product, category, model))
        result[model] = post_category

        print("Processing: ", model_html)

        if not UPDATE:
            if model_html.exists():
                print("Existing: ", model_html)
                continue

        print("Downloading")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise ConnectionError(url)

        with open(model_html, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Done!")

    with open(tm.html_dir.joinpath('product.category.model.json'), 'w', encoding='utf-8') as f_painter:
        json.dump(p_c_m, f_painter)

    tm.dumps()

    with open('Memory/category.map.json', 'w', encoding='utf-8') as f_painter:
        json.dump(result, f_painter)


if __name__ == '__main__':
    main()
