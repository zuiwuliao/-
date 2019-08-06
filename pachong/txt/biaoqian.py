
# 爬取标签
import requests
from lxml import etree
import re
import pymysql
import time

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='txtceshi', port=3306, charset='utf8mb4')
cursor = conn.cursor()      # 连接数据库及光标

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

}  # 加入请求头


def get_txt_biaoqian(urls):
    html = requests.get(urls, headers=headers)
    selector = etree.HTML(html.text)
    nums = 0

    for a in range(1, 30, 2):
        try:
            a = str(a)
            txt_biaoqian_names = '//*[@id="nav"]/ul/li[' + a + ']/a/@title'  # 标签页名字样式
            txt_biaoqian_urls = '//*[@id="nav"]/ul/li[' + a + ']/a/@href'  # 标签页url样式
            txt_biaoqian_name = selector.xpath(txt_biaoqian_names)[0]   # 标签名字
            txt_biaoqian_url = 'https://www.80txt.com' + selector.xpath(txt_biaoqian_urls)[0]   # 标签url
            pindao = 1
            nums += 1  # 目前标签序号
            print(pindao, nums, txt_biaoqian_name, txt_biaoqian_url)
            #
            # cursor.execute("insert into label (pindao,fenlei,name) values(%s,%s,%s)", (pindao, nums, txt_biaoqian_name))
            # conn.commit()

        except IndexError:
            pass
    for a in range(1, 30, 2):
        try:
            a = str(a)
            txt_biaoqian_names = '//*[@id="nav"]/ul/li[' + a + ']/a/@title'  # 标签页名字样式
            txt_biaoqian_urls = '//*[@id="nav"]/ul/li[' + a + ']/a/@href'  # 标签页url样式
            txt_biaoqian_name = selector.xpath(txt_biaoqian_names)[1]  # 标签名字
            txt_biaoqian_url = ' ' + selector.xpath(txt_biaoqian_urls)[1]  # 标签url
            pindao = 2
            nums += 1  # 目前标签序号
            print(pindao, nums, txt_biaoqian_name, txt_biaoqian_url)
            #
            # cursor.execute("insert into label (pindao,fenlei,name) values(%s,%s,%s)", (pindao, nums, txt_biaoqian_name))
            # conn.commit()

        except IndexError:
            pass





if __name__ == '__main__':
    urls = 'https://www.80txt.com/'  # 八零电子书首页
    get_txt_biaoqian(urls)