import requests
from lxml import etree
import re
import pymysql
import time

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='ceshi1', port=3306, charset='utf8mb4')
cursor = conn.cursor()      # 连接数据库及光标

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}  # 加入请求头


book_page = 'https://book.douban.com/subject/1401841/'

html = requests.get(book_page, headers=headers)
selector = etree.HTML(html.text)
try:
    nums = 97
    nums = str(nums)
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

    print('数据提取成功')

    # cursor.execute("insert into b (book_id,nums) values(%s,%s)", (id, nums))
    # cursor.execute("insert into a (book_id,title,img,author,cbs,year1,page,dingjia,Binding,isbn,score,book_jj,author_jj) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id,title,img,author,cbs,year1,page,dingjia,Binding,isbn,score,book_jj,author_jj))
    # conn.commit()
    #print( id, title, img, author, cbs, year1, page, dingjia, Binding, isbn, score, '\n', book_jj, '\n', author_jj, '\n')

except IndexError:
    pass