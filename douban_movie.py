import requests
import csv


def getJson(url):
    """
    获取网站返回来的json信息
    :param url:网页URL
    :return:若发送请求成功则返回json信息，否则返回None
    """
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def parseJson(json_text):
    """
    函数说明：解析json中的内容
    json_text:获取的json信息
    return:作为一个迭代器返回每一个电影信息
    """
    for i in range(len(json_text)):
        yield [
            json_text[i].get('rank'),
            json_text[i].get('types'),
            json_text[i].get('is_playable'),
            json_text[i].get('score'),
            json_text[i].get('title')
        ]


def write_to_file(content):
    """
    将电影信息写入douban.csv文件中
    :param content: 电影信息
    """
    with open('douban.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(content)


def main():
    for i in range(10):
        start = str(i * 20)
        target_url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=' + start + '&limit=20'
        json_text = getJson(target_url)
        for content in parseJson(json_text):
            write_to_file(content)


if __name__ == '__main__':
    main()
