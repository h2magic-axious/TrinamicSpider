import json

import fire

import Spider
import SectionSorter
import Render
import Wordpress
import Downloader
import Qiniu

description = """
Option: --arg [argument]

argument:
    spider: 
        爬取 Renference.py 中 PRODUCT 变量中的所有产品信息
        所有页面信息保存在 Memory/Trinamic_HTML 目录下
        所有产品页面下载后的路径记录汇总记录在 map.json 中
        所有产品页面的字符串进行hash编码后汇总记录在 hash.map.json 中
            
    section: 
        根据 spider 爬取到的所有页面，解析每个页面的 section 后分拣， 所有产品的有用字段保存在 Memory/Trinamic_Json 目录下
"""

function_map = {
    'spider': Spider.main,
    'section': SectionSorter.main,
    'render': Render.main,
    'wordpress': Wordpress.main,
    'download': Downloader.main,
    'qiniu': Qiniu.main
}


# 爬取HTML页面并保存到Memory/Trinamic_HTML
# Spider.main()

# 分拣处理每个HTML页面的Section
# 为每个商品输出Json格式数据
# SectionSorter.main()

# 渲染成HTML
# Render.main()

# 上传至Wordpress
# Wordpress.main()


# Downloader.main()
# Qiniu.main()
def desc():
    print(description)


def run(arg):
    func = function_map[arg]
    func()


class Run(object):
    def help(self):
        print(description)

    def run(self, arg):
        func = function_map[arg]
        func()


if __name__ == '__main__':
    fire.Fire(Run)
