# 导入webdriver API对象，可以用来调用浏览器和操作页面
from selenium import webdriver
import selenium
# 导入keys,可以使用操作键盘、标签、鼠标
from selenium.webdriver.common.keys import Keys
import time
import threading
from queue import Queue
import queue
from lxml import etree
import pymysql
import requests
import jsonpath
import sys


class DouYuCrawl(threading.Thread):
    """
    爬虫线程类,爬取每页的源码并放入解析队列中。
    """
    def __init__(self, parse_queue, crawl_queue, name):
        super(DouYuCrawl, self).__init__()
        # 每次爬取页面的个数
        self.num = 2
        # 线程名
        self.name = name
        # 爬虫队列
        self.crawl_queue = crawl_queue
        # 解析队列
        self.parse_queue = parse_queue
        # 目标链接
        self.target_url = 'https://www.douyu.com/directory/all'
        # 创建phantomJS浏览器对象
        self.driver = webdriver.PhantomJS()
        # 进入主页面
        self.driver.get(self.target_url)

    def run(self):
        print(self.name, '\tstart')
        # 页码队列非空，进行爬取信息
        while not self.crawl_queue.empty():
            self.go_to_target_page()
            for i in range(self.num):
                time.sleep(1)
                mutex.acquire()
                global crawl_page_count
                crawl_page_count += 1
                print('已爬取：', crawl_page_count, '页')
                mutex.release()
                #  将该页源码放入parse_queue 解析队列中
                self.parse_queue.put(self.driver.page_source)
                # 如果下一页可以点击，则进入到下一页，否则退出
                if self.driver.page_source.find('shark-pager-disable-next') == -1:
                    # 点击进入下一页
                    try:
                        self.driver.find_element_by_xpath('//a[@class="shark-pager-next"]').click()
                    except selenium.common.exceptions.StaleElementReferenceException as msg:
                        with open('error.txt', 'a+') as f:
                            f.write(self.name + ':重新定位元素')
                        print(msg, self.name, ':重新定位元素')
                        # 刷新界面
                        self.driver.refresh()
                        time.sleep(1)
                        self.driver.find_element_by_xpath('//a[@class="shark-pager-next"]').click()
                else:
                    break

        self.driver.quit()
        print(self.name, '\tover')

    def go_to_target_page(self):
        """
        函数说明：进入到要爬取的页面
        """
        # 取出要爬取的起始页
        num = self.crawl_queue.get()
        # 填写要跳转的页码
        try:
			# 写入页码
            self.driver.find_element_by_xpath('//input[@class="jumptxt"]').send_keys(str(num))
            time.sleep(0.1)
            # 跳转到该页面
            self.driver.find_element_by_xpath('//a[@class="shark-pager-submit"]').click()
        except selenium.common.exceptions.WebDriverException as msg:
            print(msg, self.name, ':重新输入页数')
            with open('error.txt', 'a+') as f:
                f.write(self.name + ':重新输入页数')
        except selenium.common.exceptions.StaleElementReferenceException as msg:
            print(msg, self.name, ':重新定位元素')
            with open('error.txt', 'a+') as f:
                f.write(self.name + ':重新定位元素')
        finally:
            # 刷新界面
            self.driver.refresh()
            time.sleep(1)
            # 写入页码
            self.driver.find_element_by_xpath('//input[@class="jumptxt"]').send_keys(str(num))
            time.sleep(0.1)
            # 跳转到该页面
            self.driver.find_element_by_xpath('//a[@class="shark-pager-submit"]').click()

class DouYuParser(threading.Thread):
    """
    解析线程类，从解析队列中取出页面源码，从每个页面源码中解析出所需要的信息
    """
    def __init__(self, parse_queue, name, conn, cursor):
        super(DouYuParser, self).__init__()
        # 线程名
        self.name = name
        # 解析队列
        self.parse_queue = parse_queue
        # 数据库链接
        self.conn = conn
        # 游标
        self.cursor = cursor

    def run(self):
        print(self.name, '\tstart')
        # 若爬虫线程未运行完毕，或者解析队列不为空，均不能退出程序
        while not self.parse_queue.empty():
            try:
                # 从解析队列中取出页面源代码
                html = self.parse_queue.get(False)
            except queue.Empty as e:
                with open('error.txt', 'a+') as f:
                    f.write(str(e))
                pass
            try:
                # 解析html文档为HTML DOM模型
                html = etree.HTML(html)
                # 用xpath解析出每个节点
                items = html.xpath('//ul[@id="live-list-contentbox"]//li//a')
                # 解析出每个节点的具体信息
                for item in items:
                    data = []
                    # 直播类型
                    data.append(item.xpath('.//span[@class="tag ellipsis"]/text()')[0])
                    # 房间号
                    data.append(item.xpath('./@data-rid')[0])
                    # 房主名称
                    data.append(item.xpath('.//span[@class="dy-name ellipsis fl"]/text()')[0])
                    # 房间名称
                    data.append(item.xpath('.//@title')[0])
                    # 热度
                    data.append(item.xpath('.//span[@class="dy-num fr"]/text()')[0])
                    # print(data)
					# 写入数据库
                    self.writeDatas(data)
                mutex.acquire()
                global crawl_page_count
                crawl_page_count += 1
                print('已解析：', crawl_page_count, '页')
                mutex.release()
            except Exception as e:
                print('2---',  e)
                with open('error.txt', 'a+') as f:
                    f.write(str(e))

        print(self.name, '\tover')

    def writeDatas(self, data):
		"""
        函数说明：将爬取到的数据写入数据库
		data：数据列表
        """
        parm = data
        sql = 'insert into room_message values(%s, %s, %s, %s, %s)'
        try:
            mutex.acquire()
            self.cursor.execute(sql, parm)
            self.conn.commit()
            mutex.release()
        except Exception as e:
            with open('error.txt', 'a+') as f:
                f.write(str(e))
            print('3---', parm)
            print('3---', e)


# 已爬取页数
crawl_page_count = 0
# 已解析页数
parse_page_count = 0
# 爬虫队列，存放待爬取的页码
crawl_queue = Queue()
# 解析队列，存放待解析的源码
parse_queue = Queue()
# 线程互斥锁，操作数据库
mutex = threading.Lock()


def main():
	# 连接数据库
    try:
        conn = pymysql.connect(host='localhost', user='root', password='ljg', db='douYu', charset='utf8')
        cursor = conn.cursor()
    except Exception as e:
        with open('error.txt', 'a+') as f:
            f.write(str(e))
        print('1---', e)
    # 进入第一页查看共有多少页
    target_url = 'https://www.douyu.com/gapi/rkc/directory/0_0/1'
	# 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
    }
    response = requests.get(target_url, headers=headers)
    json_info = response.json()
    page_num = jsonpath.jsonpath(json_info, '$.data.pgcnt')[0]
    print('共:', page_num, '页')
    # 每隔10页创建一个页码
    for num in range(1, int(page_num), 10):
        crawl_queue.put(num)

    # 线程列表，存放所有创建的线程
    thread_list = []
    # 爬虫线程
    crawl_name = ['爬虫线程1', '爬虫线程2', '爬虫线程3']
    for name in crawl_name:
        crawl = DouYuCrawl(parse_queue=parse_queue, crawl_queue=crawl_queue, name=name)
        crawl.start()
        thread_list.append(crawl)

    # 解析线程
    parse_name = ['解析线程1', '解析线程2', '解析线程3']
    for name in parse_name:
        parse = DouYuParser(parse_queue=parse_queue, name=name, conn=conn, cursor=cursor)
        parse.start()
        thread_list.append(parse)

    print('线程创建完毕！')
    for thread in thread_list:
        # 线程阻塞，主线程等待子线程运行
        thread.join()

    # 关闭数据库
    cursor.close()
    conn.close()
    print('work done!')


if __name__ == '__main__':
    main()
