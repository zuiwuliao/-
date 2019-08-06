

# 书籍详情依次爬取（按照标签顺序）并存储到MySQL

import requests
from lxml import etree
import re
import pymysql
import time

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='ceshi1', port=3306, charset='utf8mb4')
cursor = conn.cursor()      # 连接数据库及光标

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/72.0.3626.121 Safari/537.36'
}  # 加入请求头



def get_book_biaoqian(urls):
    html = requests.get(urls, headers=headers)
    selector = etree.HTML(html.text)
    nums = 0
    for a in range(1, 7):
        for b in range(1, 10):
            for c in range(1, 5):
                try:
                    a = str(a)
                    b = str(b)
                    c = str(c)
                    book_biaoqians = '//*[@id="content"]/div/div[1]/div[2]/div[' + a + ']/table/tbody/tr[' + b + ']/td[' + c + ']/a/@href'  # 标签页总样式
                    book_biaoqian = 'https://book.douban.com' + selector.xpath(book_biaoqians)[0]  # 每个标签对应的子网站链接
                    nums += 1  # 目前标签序号
                    print(nums, book_biaoqian, a)
                    get_book_biaoqian_page(book_biaoqian, nums)   # 寻找标签页中，列表地址

                except IndexError:
                    pass


def get_book_biaoqian_page(book_biaoqian, nums):
    for i in range(0, 100, 20):
        i = str(i)
        book_biaoqian_page = book_biaoqian + '?start=' + i + '&type=T'
        print(book_biaoqian_page)
        get_book_list(book_biaoqian_page, nums)   # 寻找每个图书的详情页地址


def get_book_list(book_biaoqian_page,nums):
    html = requests.get(book_biaoqian_page, headers=headers)
    selector = etree.HTML(html.text)
    try:
        for d in range(1, 21):
            d = str(d)
            book_pages = '//*[@id="subject_list"]/ul/li[' + d + ']/div[2]/h2/a/@href'
            book_page = selector.xpath(book_pages)[0]
            print(book_page)
            get_book_xiangqing(book_page, nums)

    except IndexError:
        pass


def get_book_xiangqing(book_page, nums):

    html = requests.get(book_page, headers=headers)

    selector = etree.HTML(html.text)

    try:
        id = re.findall('\d+', book_page)[0]    # 图书ID
        title = re.findall('<span property="v:itemreviewed">(.*?)</span>',html.text,re.S)[0]  # 书名
        img = selector.xpath('//*[@id="mainpic"]/a/img/@src')[0]    # 图片
        # replace('a', 'b')将a替换为b
        author = re.findall('作者:{0,1}</span>.*?>(.*?)</a>',html.text,re.S)[0].replace(' ', '').replace('\n', '')   # 作者
        cbs = re.findall('出版社:</span>(.*?)<br/>',html.text,re.S)[0].replace(' ', '').replace('\n', '')  # 出版社
        year1 = re.findall('出版年:</span>(.*?)<br/>',html.text,re.S)[0].replace(' ', '').replace('\n', '') # 出版年
        page = re.findall('页数:</span>(.*?)<br/>',html.text,re.S)[0].replace(' ', '').replace('\n', '')  # 页码
        dingjia = re.findall('定价:</span>(.*?)<br/>',html.text,re.S)[0].replace(' ', '').replace('\n', '')   # 定价
        Binding = re.findall('装帧:</span>(.*?)<br/>',html.text,re.S)[0].replace(' ', '').replace('\n', '')   # 装帧
        isbn = re.findall('ISBN:</span>(.*?)<br/>',html.text,re.S)[0].replace(' ', '').replace('\n', '')    # ISBN
        score = selector.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0].replace(' ', '')   # 评分
        book_jj = re.findall('内容简介.*?class="a?l?l? ?h?i?d?d?e?n? ?".*?<div class="intro">(.*?)</div>',html.text,re.S)[0].replace(' ', '').replace('\n', '')  # 图书简介
        author_jj = re.findall('作者简介.*?class="a?l?l? ?h?i?d?d?e?n? ?".*?<div class="intro">(.*?)</div>',html.text,re.S)[0].replace(' ', '').replace('\n', '')   # 作者简介



        # cursor.execute("insert into a (book_id,title,img,author,cbs,year1,page,dingjia,Binding,isbn,score,book_jj,author_jj) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id,title,img,author,cbs,year1,page,dingjia,Binding,isbn,score,book_jj,author_jj))
        # cursor.execute("insert into b (book_id,nums) values(%s,%s)", (id, nums))
        # conn.commit()

        print(nums, id, title, img, author, cbs, year1, page, dingjia, Binding, isbn, score, '\n', book_jj, '\n', author_jj, '\n')

        time.sleep(2)



    except IndexError:
        pass


if __name__ == '__main__':
    urls = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'  # 豆瓣图书标签页
    get_book_biaoqian(urls)



