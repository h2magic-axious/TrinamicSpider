from pathlib import Path
import json

from bs4 import BeautifulSoup

from Reference import format_data, TRINAMIC_ROOT, format_value
from Memory import FieldMemory, PictureMemory, ResourceMemory, JsonMemory

TITLE = 'title'
DIA_PIN = 'Block Diagram / Pinout'
DOWNLOADS = 'Downloads'
TECHNIQUE = 'Technical Details'


def from_tr_get_element(tr: BeautifulSoup):
    tmp = tr.find('td')
    return tmp.text.strip(), TRINAMIC_ROOT + tmp.find('a')['href']


class Sorter:
    def __init__(self, html_path):
        self.model = html_path
        self.sections = None
        self.result = None

        with open(html_path, 'r', encoding='utf-8') as f:
            self.parser = BeautifulSoup(f.read(), 'lxml')

        self.__get_sections()
        self.__format()

    def __get_sections(self):
        self.sections = self.parser.find_all('section')

    def __format(self):
        self.result = format_data(self.sections)

    def get_excerpt(self):
        return self.result['title'].text

    def get_dia_pin(self):
        dia_pin = self.result.get(DIA_PIN, None)
        if dia_pin:
            return [TRINAMIC_ROOT + img['src'] for img in dia_pin.find_all('img')]
        else:
            return None

    def get_resource(self):
        downloads = self.result.get(DOWNLOADS, None)
        if downloads is None:
            return None

        downloads_title = downloads.find_all('h3')
        tbodys = downloads.find_all('tbody')

        return {
            title.text: [from_tr_get_element(tr) for tr in tbody.find_all('tr')]
            for title, tbody in zip(downloads_title, tbodys)
        }

    def get_fields(self):
        technique = self.result.get(TECHNIQUE, None)
        if technique is None:
            return None

        # ths 的数量，就表示当前页面下的产品Item种类的数量
        ths = technique.find_all('th')[1:]
        try:
            items = [(th.text, th.find('img')['src']) for th in ths]
        except:
            items = [(th.text, self.result['title'].find('img')['src']) for th in ths]

        records = [tr.find_all('td') for tr in technique.find('tbody').find_all('tr')]
        # 产品的参数
        fields = [r[0].text for r in records]

        result = dict()
        for index, item in enumerate(items):
            index += 1
            model, src = item
            detail = {field: format_value(r[index]) for field, r in zip(fields, records)}
            detail['picture'] = TRINAMIC_ROOT + src
            result[model] = detail

        return result


def export_json(model, excerpt, field_dict: dict, pm: PictureMemory, rm: ResourceMemory):
    result = {
        'model': model,
        'excerpt': excerpt,
    }

    model_json = model + '.json'

    field = field_dict[model]
    title_picture = field.pop('picture')

    picture_path = pm.picture_dir.joinpath(model_json)
    if picture_path.exists():
        with open(picture_path, 'r', encoding='utf-8') as f_picture_temp:
            pictures = json.load(f_picture_temp)
    else:
        pictures = []

    resource_path = rm.resource_dir.joinpath(model_json)
    if resource_path.exists():
        with open(resource_path, 'r', encoding='utf-8') as f_resource_temp:
            resources = json.load(f_resource_temp)
    else:
        resources = dict()

    result.update({
        'fields': field,
        'picture': title_picture,
        'images': pictures,
        'resource': resources
    })

    return result


def main():
    pm = PictureMemory()
    rm = ResourceMemory()
    fm = FieldMemory()
    jm = JsonMemory()

    with open('Memory/Trinamic_HTML/map.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for model, path in data.items():
        sorter = Sorter(path)
        try:
            pm.insert(model, sorter.get_dia_pin())
        except:
            pass

        try:
            rm.insert(model, sorter.get_resource())
        except:
            pass

        try:
            fm.insert(model, sorter.get_fields())
        except:
            pass

    pm.dumps()
    rm.dumps()
    fm.dumps()

    with open('Memory/Trinamic_Fields/map.json', 'r', encoding='utf-8') as f:
        fields = json.load(f)

    for model, path in data.items():
        sorter = Sorter(path)

        try:
            jm.insert(model, export_json(model, sorter.get_excerpt(), fields, pm, rm))
        except:
            pass

    jm.dumps()

if __name__ == '__main__':
    main()