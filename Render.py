import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from translator import translate

from quicktranslate import get_translate_google

from Memory import FileSystem
from Reference import format_url

RESOURCE = {
    'Datasheet': '产品规格书',
    'Documentation': '用户手册',
    'Quality': '质量声明',
    'Software': '软件',
    'PCNs': '产品变更声明',
    'Application Notes': '产品应用笔记'
}
STATUS = {
    'active': '量产',
    'on hold': '暂停',
    'preview': '试产'
}

TEMPLATES = FileSystem.memory.joinpath('Templates')


def format_resource_key(key):
    result = RESOURCE.get(key.strip(), None)
    if result is None:
        return key
    return result


class Render:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def __get_template(self, path):
        return self.env.get_template(path)

    def render(self, template, item_model, item_data: dict):
        # Template's argv
        # model, picture, excerpt, fields, images, resources

        if item_data is None:
            return self.__render(template, {})
        print('Render', item_model)

        fields = item_data.get('fields', None)
        if fields:
            status: str = fields.pop('Status')
            fields['产品状态'] = STATUS.get(status.lower(), status)

        resources: dict = item_data.get('resource', None)
        if resources:
            result = {format_resource_key(key): [(n.strip(), format_url(v)) for n, v in values] for key, values in
                      resources.items()}
        else:
            result = None

        images = item_data.get('images', None)
        if images is None:
            imgs = []
        else:
            imgs = [format_url(url) for url in images]

        context = {
            'model': item_model,
            'picture': format_url(item_data.get('picture', None)),
            'excerpt': translate(item_data.get('excerpt', 'No excerpt')),
            'fields': fields,
            'images': imgs,
            'resources': result
        }

        return self.__render(template, context)

    def __render(self, path, dt: dict):

        template = self.__get_template(path)
        return template.render(**dt)


def main():
    with open('Memory/Trinamic_Json/map.json', 'r', encoding='utf-8') as f:
        tmc_items: dict = json.load(f)

    render = Render()

    render_html_dir = FileSystem.memory.joinpath('Trinamic_Render')
    render_html_dir.mkdir(exist_ok=True)

    for model, content in tmc_items.items():
        text = render.render('Article.html', model, content)
        with open(render_html_dir.joinpath(model + '.html'), 'w', encoding='utf-8') as f:
            f.write(text)


if __name__ == '__main__':
    main()
