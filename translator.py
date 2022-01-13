from random import randint
from hashlib import md5
import urllib

import requests

API_HOST = {
    'http': 'http://api.fanyi.baidu.com/api/trans/vip/translate',
    'https': 'https://fanyi-api.baidu.com/api/trans/vip/translate'
}

FROM = 'en'
TO = 'zh'

APPID = '20200301000390841'
SECRET_KEY = '6DXuIYHuPjxrR06OTRoQ'


def encryption(func):
    def en(*args, **kwargs):
        content = func(*args, **kwargs)
        return md5(content.encode('utf-8')).hexdigest()

    return en


@encryption
def sign(query, salt):
    return f"{APPID}{query}{salt}{SECRET_KEY}"


def translate(content):
    salt = randint(32768, 65535)
    _sign = sign(content, salt)
    url = f"{API_HOST['http']}?appid={APPID}&q={urllib.parse.quote(content)}&from=en&to=zh&salt={salt}&sign={_sign}"
    try:
        response = requests.get(url).json()
        return response['trans_result'][0]['dst']
    except:
        return content


if __name__ == '__main__':
    r = translate(
        "For a quick evaluation of one of the Trinamic Breakout Boards (BOBs) without commiting to a processor, the USB-2-SD translates TMCL-IDE commands into Step/Direction pulses. Simply connect it directly via the USB type A compatible PCB footprint to your computer to communicate with the breakout board of your choice via S/D.Featuring Trinamic's TMC4330A-LA fully integrated stepper motor servo controller, the USB-2-SD allows for the flexible acceleration profiles of linear ramping, SixPoint\u2122 ramping, and S-shaped ramping. In addition, an incremental encoder (5V signal level) can be connected to the USB-2-SD to read back motor or joint position.The simple but powerful Step/Dir signal generator\u00a0can be controlled via Trinamic\u2019s TMCL protocol and commands, and is fully supported by the TMCL-IDE graphical user interface.")

    print(r)
