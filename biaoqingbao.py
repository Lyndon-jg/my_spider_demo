import requests
from lxml import etree
import os

project_dir = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_dir, 'images')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}


def do_request(url):
    # 发出请求
    response = requests.get(url, headers)
    parse(response)


def parse(response):
    # 解析返回的页面
    html = response.text
    html_dom = etree.HTML(html)
    imgs = html_dom.xpath('//div[@class="page-content text-center"]/div/a/img/@data-original')
    download(imgs)


def download(imgs):
    # 下载图片
    for each_img in imgs:
        img_content = requests.get(url=each_img, headers=headers)
        img_name = each_img[-10:]
        with open(os.path.join(IMAGES_STORE, img_name), 'wb') as f:
            f.write(img_content.content)


if __name__ == '__main__':
    url = 'http://www.doutula.com/photo/list/?page='
    page = input('please input pages:')
    for i in range(1, int(page) + 1):
        do_request(url)
        print('page:', i, ' download ok！')

