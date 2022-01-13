import json

from Memory import ResourceMemory, FileSystem
from Reference import request


class DownloadMemory(FileSystem):
    def __init__(self):
        self.download_dir = self.memory.joinpath('Download_Resource')
        self.download_dir.mkdir(exist_ok=True)
        self.rm = ResourceMemory()

    def insert(self, url: str):
        name = url.split('/')[-1]
        print("Downloading: ", url)

        file_path = self.download_dir.joinpath(name)
        if file_path.exists():
            print("Existing")
            return

        response = request(url)

        with open(file_path, 'wb') as f:
            f.write(response.content)

    def iter_resource(self):
        with open(self.rm.resource_dir.joinpath('map.json'), 'r', encoding='utf-8') as f:
            resource_list = json.load(f)

        for name, url in resource_list:
            yield name.strip(), url


def main():
    dm = DownloadMemory()

    # download picture
    with open('Memory/Trinamic_Fields/map.json', 'r', encoding='utf-8') as f:
        picutres = [item.get('picture', None) for _, item in json.load(f).items()]

    total_number = len(picutres)
    index = 1
    for picture in picutres:
        print("Title, 共计: ", total_number, "当前: ", index)
        dm.insert(picture)
        index += 1

    # download pid and dia picture
    with open('Memory/Trinamic_Picture/map.json', 'r', encoding='utf-8') as f:
        dia_pin_list = json.load(f)

    total_number = len(dia_pin_list)
    index = 1
    for dp in dia_pin_list:
        print("Picture, 共计: ", total_number, "当前: ", index)
        dm.insert(dp)
        index += 1

    # download resource
    with open('Memory/Trinamic_Resource/map.json', 'r', encoding='utf-8') as f:
        resources = json.load(f)

    total_number = len(resources)
    index = 1

    for _, url in resources:
        print("Resource, 共计: ", total_number, "当前执行: ", index)
        dm.insert(url)
        index += 1


if __name__ == '__main__':
    main()
