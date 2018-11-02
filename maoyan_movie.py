import requests
import re
import json
import time


def get_html(target_url):
    """
    函数说明：获取网页源码
    target_url:网页URL
    return:若发送请求成功则返回网页源码，否则返回None
    """
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
    }
    response = requests.get(url=target_url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_html(html):
    """
    函数说明：用re解析网页
    html:网页源码 ，字符串类型
    return:作为一个迭代器返回每一个电影信息
    """
	# 匹配模式
    pattern = re.compile(r'<dd>.*?board-index-.*?>(.*?)</i>.*?data-src="(.*?)".*?</a>.*?name.*?title="(.*?)".*?</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>', re.S)
    movies_info = re.findall(pattern=pattern, string=html)
    for movie_info in movies_info:
        yield {
            'rank': movie_info[0],
            'movie_pic': movie_info[1],
            'title': movie_info[2],
            'stars': movie_info[3].strip()[3:],
            'time': movie_info[4].strip()[5:],
            'score': movie_info[5] + movie_info[6]
               }


def write_to_file(movie_info):
    """
    函数说明：将电影信息写入本地movie_info.txt文件
    movie_info:电影信息，字典类型
    """
    # encoding='utf-8'，避免写入时失败
    with open('movies_info.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(movie_info, ensure_ascii=False) + '\n')


def main():
    for i in range(10):
        time.sleep(1)
        # 拼接URL
        target_url = 'http://maoyan.com/board/4?offset=' + str(i * 10)
        # 获取网页源码
        html = get_html(target_url)
        # 取出每一条电影信息，写入本地文件
        for movie_info in parse_html(html):
            print(movie_info)
            write_to_file(movie_info)


if __name__ == '__main__':
    main()
