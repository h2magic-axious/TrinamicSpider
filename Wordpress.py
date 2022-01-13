import json

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPost, EditPost, NewPost

import requests

from Memory import FileSystem


class CONST:
    USERNAME = 'nickname'
    PASSWORD = 'Ignore009'
    ROOT_URL = 'https://chiplinkstech.com'
    XML_API = ROOT_URL + '/xmlrpc.php'
    JSON_API = ROOT_URL + '/wp-json/wp/v2'
    AUTHOR = 17


DRAFT = 'draft'
PRIVATE = 'private'
PUBLISH = 'publish'


class WordPress:
    def __init__(self):
        self.__client = Client(CONST.XML_API, CONST.USERNAME, CONST.PASSWORD)

    def terms(self, tag, category):
        return {
            'post_tag': [tag],
            'category': [category]
        }

    def call(self, *args, **kwargs):
        return self.__client.call(*args, **kwargs)

    def get_post_number(self):
        url = f"{CONST.JSON_API}/posts?author={CONST.AUTHOR}&per_page=1"
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(url)

        return response.headers['x-wp-total']

    def post_map(self):
        post_number = int(self.get_post_number())
        page, other = divmod(post_number, 100)
        if other:
            page += 1

        result = dict()

        for i in range(1, page + 1):
            url = f"{CONST.JSON_API}/posts?author=17&per_page=100&page={i}"
            response = requests.get(url)
            if response.status_code != 200:
                raise ConnectionError(url)

            for post in response.json():
                result[post['title']['rendered']] = post['id']

        return result

    def new_post(self, title, content, category):
        post = WordPressPost()
        post.title = title
        post.content = content

        post.terms_names = self.terms(title, category)

        post.post_status = PUBLISH
        self.call(NewPost(post))

    def edit_post(self, post_id, title, content, category):
        post = self.call(GetPost(post_id))
        post.content = content
        post.terms_names = self.terms(title, category)
        self.call(EditPost(post_id, post))


def main():
    wp = WordPress()
    post_map = wp.post_map()

    with open('Memory/category.map.json', 'r', encoding='utf-8') as f_painter:
        category_map = json.load(f_painter)

    for render_html in FileSystem.memory.joinpath('Trinamic_Render').iterdir():
        with open(render_html, 'r', encoding='utf-8') as f:
            text = f.read()

        file_name = render_html.name.split('.')[0]
        ident = post_map.get(file_name, None)
        category = category_map.get(file_name, '产品详情')

        if ident is None:
            print("New Post: ", file_name)
            wp.new_post(file_name, text, category)
        else:
            print("Edit Post: ", file_name)
            wp.edit_post(ident, file_name, text, category)


if __name__ == '__main__':

    from bs4 import BeautifulSoup

    wp = WordPress()
    number = int(wp.get_post_number())
    page, other = divmod(number, 100)
    if other:
        page += 1

    result = dict()

    for i in range(1, page + 1):
        url = f"{CONST.JSON_API}/posts?per_page=100&page={i}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(url)

        for post in response.json():
            result[post['title']['rendered']] = post['id']

    # result[ 标贴 ] = post_id

    file = open("record1.txt", 'w', encoding='utf-8')

    for title, post_id in result.items():
        post_url = f"{CONST.JSON_API}/posts/{post_id}"
        post_response = requests.get(post_url)
        if post_response.status_code != 200:
            file.writelines(f"{title} is bed, Link: {post_url}")
            continue

        data = post_response.json()
        print(f"Parse: {post_url}")
        post_soup = BeautifulSoup(data['content']['rendered'], 'lxml')
        tag_a_list = [a['href'] for a in post_soup.find_all('a')]
        tag_img_list = [img['src'] for img in post_soup.find_all('img')]

        url_list = []

        for link in tag_a_list + tag_img_list:
            print(f" {title}: Check link: {link}")
            if '#' in link:
                continue
            check_response = requests.get(link)
            if check_response.status_code != 200:
                url_list.append(link)
                print(f"  {title}, {data['link']}: {link} is failed")
                continue

        if url_list:
            file.writelines(f"{title}:{data['link']} failed urls:\n")
            for ul in url_list:
                file.writelines(f"    {ul}\n")

    file.close()
