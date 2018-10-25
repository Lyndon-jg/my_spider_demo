import re
import requests
from lxml import etree


class NetbianPic(object):
    """
    下载www.netian.com网站壁纸
    """
    def __init__(self, category, page):
        # 图片种类
        self.category = category
        # 总页数
        self.page = page
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}
        self.proxies = {"https": '106.75.226.36:808'}
        self.target_url = 'http://www.netbian.com'
        # 每页URL，拼接形成
        self.page_url = ''
        # 图片所在页面URL
        self.pic_page_url = []
        # 图片URL
        self.pic_url = ''

    def downloadStart(self):
        """
        函数说明：开始下载函数
        """
        for p in range(1, self.page + 1):
            if p == 1:
                self.page_url = self.target_url + self.category + 'index.htm'
            else:
                self.page_url = self.target_url + self.category + 'index_' + str(p) + '.htm'
            print(self.page_url)
            self.getPicUrl(url=self.page_url)

    def getPicUrl(self, url):
        """
        函数说明：获得每页中所有图片的url
        URL：页面URL
        """
        response = requests.get(url=url, headers=self.headers)
        # print(response.url)
        # print(response.status_code)
        # print(response.encoding)
        # 设置编码，否则response.text编码有问题
        response.encoding = 'gbk'
        html = response.text
        # 解析html为HTML DOM模型
        # html = etree.HTML(html)
        # 通过xpath解析源出图片页面
        # self.pic_page_url = html.xpath('//div[@class="list"]/ul/li/a/@href')
        self.pic_page_url = re.findall(r'href="(/desk/\d+.htm)"', html)
        # 从源图片页面URL找图片URL
        for page in self.pic_page_url:
            pic_page = self.target_url + page
            response = requests.get(url=pic_page, headers=self.headers)
            response.encoding = 'gbk'
            html = response.text
            # 解析html为HTML DOM模型
            html = etree.HTML(html)
            # 通过xpath解析出图片链接（此图片为960x450像素的，更高像素的还在下一层的下一层。。。懒得弄了）
            self.pic_url = html.xpath('//div[@class="pic"]/p/a/img/@src')[0]
            self.writePic(self.pic_url)

    def writePic(self, url):
        """
        函数说明：下载图片到本地
        url:图片URL
        """
        response = requests.get(url=url, headers=self.headers)
        filename = url[-10:]
        with open(filename, 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    categorys = {
        '风景': '/fengjing/',
        '美女': '/meinv/',
        '日历': '/rili/',
        '游戏': '/youxi/',
        '动漫': '/dongman/',
        '唯美': '/weimei/',
        '可爱': '/keai/',
        '设计': '/sheji/',
        '汽车': '/qiche/',
        '花卉': '/huahui/',
        '动物': '/dongwu/',
        '节日': '/jieri/',
        '人物': '/renwu/',
        '美食': '/meishi/',
        '水果': '/shuiguo/',
        '建筑': '/jianzhu/',
        '影视': '/yingshi/',
        '体育': '/tiyu/',
        '军事': '/junshi/',
        '非主流': '/feizhuliu/',
        '其他': '/qita/',
        '王者荣耀': '/s/wangzherongyao/',
        '护眼': '/s/huyan/',
        '鬼刀': '/s/guidao/'
    }
    title = []
    for k, v in categorys.items():
        title.append(k)
    print(title)
    # 下载图片类型
    category = input("input download category:")
    # 下载页数
    page = input("input pages:")
    # 创建对象
    p = NetbianPic(categorys.get(category), int(page))
    p.downloadStart()