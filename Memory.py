from pathlib import Path
import json

from Reference import format_name

BASE_DIR = Path(__file__).parent.resolve()


class FileSystem:
    memory = BASE_DIR.joinpath('Memory')


class TrinamicMemory(FileSystem):
    def __init__(self):
        self.html_dir = self.memory.joinpath('Trinamic_HTML')
        self.html_dir.mkdir(exist_ok=True)

    def run(self, insert: bool, *args):
        # insert is True means: Insert a directory's path
        # insert is False means: Get this directory's path

        res_dir = self.html_dir
        for arg in args:
            res_dir /= arg

        if insert:
            res_dir.mkdir(parents=True, exist_ok=True)

        return res_dir

    def product(self, insert, product):
        return self.run(insert, format_name(product))

    def category(self, insert, product, category):
        return self.run(insert, format_name(product), format_name(category))

    def item(self, insert, product, category, item):
        return self.run(insert, format_name(product), format_name(category), item)

    def dumps(self):
        result = dict()
        for product in self.html_dir.iterdir():
            if product.name in ['map.json', 'hash.map.json', 'update.record.json', 'product.category.model.json']:
                continue
            for category in product.iterdir():
                for item in category.iterdir():
                    model = item.name.split('.')[0]
                    result[model] = item.as_posix()

        with open(self.html_dir.joinpath('map.json'), 'w', encoding='utf-8') as f:
            json.dump(result, f)


class FieldMemory(FileSystem):
    def __init__(self):
        self.field_dir = self.memory.joinpath('Trinamic_Fields')
        self.field_dir.mkdir(exist_ok=True)

    def insert(self, item, data):
        item_path = self.field_dir.joinpath(item + '.json')
        with open(item_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def dumps(self):
        f = open(self.field_dir.joinpath('map.json'), 'w', encoding='utf-8')
        datas = dict()
        for model in self.field_dir.iterdir():
            if model.name == 'map.json':
                continue

            with open(self.field_dir.joinpath(model), 'r', encoding='utf-8') as f_temp:
                data = json.load(f_temp)

            for key, value in data.items():
                if key not in datas:
                    datas[key] = value

        json.dump(datas, f)

        f.close()


class PictureMemory(FileSystem):
    def __init__(self):
        self.picture_dir = self.memory.joinpath('Trinamic_Picture')
        self.picture_dir.mkdir(exist_ok=True)

    def insert(self, item, images):
        with open(self.picture_dir.joinpath(item + '.json'), 'w', encoding='utf-8') as f:
            json.dump(images, f)

    def dumps(self):
        fp = open(self.picture_dir.joinpath('map.json'), 'w', encoding='utf-8')
        history = []
        for model in self.picture_dir.iterdir():
            if model.name == 'map.json':
                continue
            with open(self.picture_dir.joinpath(model), 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data is None:
                continue

            for value in data:
                if value in history:
                    continue

                history.append(value)

        json.dump(history, fp)
        fp.close()


class ResourceMemory(FileSystem):
    def __init__(self):
        self.resource_dir = self.memory.joinpath('Trinamic_Resource')
        self.resource_dir.mkdir(exist_ok=True)

    def insert(self, item, datas: dict):
        with open(self.resource_dir.joinpath(item + '.json'), 'w', encoding='utf-8') as f:
            json.dump(datas, f)

    def dumps(self):
        fp = open(self.resource_dir.joinpath('map.json'), 'w', encoding='utf-8')
        history = []

        for model in self.resource_dir.iterdir():
            if model.name == 'map.json':
                continue

            with open(self.resource_dir.joinpath(model), 'r', encoding='utf-8') as f:
                data = json.load(f)

            for key, values in data.items():
                for value in values:
                    if value in history:
                        continue
                    history.append(value)

        json.dump(history, fp)
        fp.close()


class JsonMemory(FileSystem):
    def __init__(self):
        self.json_dir = self.memory.joinpath('Trinamic_Json')
        self.json_dir.mkdir(exist_ok=True)

    def insert(self, model, datas):
        with open(self.json_dir.joinpath(model + '.json'), 'w', encoding='utf-8') as f:
            json.dump(datas, f)

    def dumps(self):
        fp = open(self.json_dir.joinpath('map.json'), 'w', encoding='utf-8')
        datas = dict()

        for model in self.json_dir.iterdir():
            if model.name == 'map.json':
                continue

            with open(self.json_dir.joinpath(model), 'r', encoding='utf-8') as f:
                data = json.load(f)

            model = data.pop('model')
            if model not in datas:
                datas[model] = data

        json.dump(datas, fp)
        fp.close()
