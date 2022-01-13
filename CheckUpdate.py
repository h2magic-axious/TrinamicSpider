import json, hashlib

from Memory import TrinamicMemory
from Spider import MainPage
from Reference import request


class CheckUpdater:
    def __init__(self):
        self.tm = TrinamicMemory()
        self.hash = hashlib.sha256()

    def iter(self):
        with open(self.tm.html_dir.joinpath('map.json'), 'r', encoding='utf-8') as f_painter:
            data_list = json.load(f_painter)

        for key, value in data_list.items():
            yield key, value

    def code_html(self, html_text: str):
        self.hash.update(html_text.encode('utf-8'))
        return self.hash.hexdigest()

    def get_hash_map(self):
        with open(self.tm.html_dir.joinpath('hash.map.json'), 'r', encoding='utf-8') as f_painter:
            hash_map = json.load(f_painter)
        return hash_map

    def dumps(self):
        results = dict()
        for key, value in self.iter():
            with open(value, 'r', encoding='utf-8') as f:
                text = f.read()

            results[key] = self.code_html(text)

        with open(self.tm.html_dir.joinpath('hash.map.json'), 'w', encoding='utf-8') as f_painter:
            json.dump(results, f_painter)


def is_updated(cu: CheckUpdater, mp: MainPage):
    hash_map = cu.get_hash_map()
    is_update = False
    for product, post_category, category, model, url in mp.iter():
        response = request(url)
        hash_code = cu.code_html(response.text)
        print(hash_code)
        if model not in hash_map or hash_map[model] != hash_code:
            print("Update page: ", model)
            is_update = True

    return is_update


if __name__ == '__main__':
    cu = CheckUpdater()
    # 为每个页面编码
    # cu.dumps()

    # 检查更新
    mp = MainPage()

    if is_updated(cu, mp):
        # main()
        print("Is Update")
