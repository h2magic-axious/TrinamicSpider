"""
TMC2225-SA-T

TMC223-LI
TMC223-SI
TMCS-28-6.35-10000-AT-01
TMCS-28-6.35-1024-AT-01
TMCS-40-6.35-10000-AT-01
"""
import json
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape

from Memory import FileSystem
from Reference import QINIU_DNS_NAME
from Wordpress import WordPress

RESOURCE = {
    'Datasheet': '产品规格书',
    'Documentation': '用户手册',
    'Quality': '质量声明',
    'Software': '软件',
    'PCNs': '产品变更声明',
    'Application Notes': '产品应用笔记'
}


def format_resource_key(key):
    result = RESOURCE.get(key.strip(), None)
    if result is None:
        return key
    return result


def format_url(name):
    return QINIU_DNS_NAME + name


DIR = Path(__file__).parent.joinpath('Memory').joinpath('temp').absolute()
RENDER_DIR = DIR.joinpath('HTML')
RENDER_DIR.mkdir(exist_ok=True)

with open(DIR.joinpath("map.json"), 'r', encoding='utf-8') as f:
    demos = []
    dicts = json.load(f)
    for model in dicts:
        values = dicts[model]
        values['model'] = model
        demos.append(values)


def render(contexts: List[dict]):
    env = Environment(
        loader=FileSystemLoader(FileSystem.memory.joinpath('Templates')),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('Article.html')
    wp = WordPress()

    for context in contexts:
        model = context['model']
        print(f"Rendering: {model}\n")
        resource: dict = context.get('resource', None)
        if resource:
            result = {
                format_resource_key(key): [(name.strip(), format_url(value)) for name, value in values] for key, values
                in resource.items()
            }

        else:
            result = None

        images = context.get('images', None)
        if images is None:
            img = []
        else:
            img = [format_url(url) for url in images]

        text = template.render({
            'model': model,
            'picture': format_url(context['picture']),
            'excerpt': context['excerpt'],
            'fields': context['fields'],
            'images': img,
            'resources': result
        })

        print("Uploading: ", model)
        wp.new_post(model, text, '产品详情')


if __name__ == '__main__':
    render(demos)
