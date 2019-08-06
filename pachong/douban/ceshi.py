
import requests
from lxml import etree
import re
import pymysql
import time
a = 'ds fgg"124hgd  5"  gfsdgh'
year = re.findall('ds(.*?)gh', a)[0].replace(' ', '').replace('\n', '')  # 出版年

print(year)



















#
#
# # 书籍详情依次爬取（按照标签顺序）并存储到MySQL
#
# import requests
# from lxml import etree
# import re
# import pymysql
# import time
#
# # conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='b')
# # cursor = conn.cursor()      # 连接数据库及光标
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3641.400 QQBrowser/10.4.3284.400'}  # 加入请求头
#
# urls = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'  # 豆瓣图书标签页
#
# html = requests.get(urls,headers=headers)
# selector = etree.HTML(html.text)
#
# # 序号
# nums = 0
# for a in range(1,7):
#     for b in range(1,10):
#         for c in range(1,5):
#             try:
#                 a = str(a)
#                 b = str(b)
#                 c = str(c)
#
#                 url = '//*[@id="content"]/div/div[1]/div[2]/div[' + a + ']/table/tbody/tr[' + b + ']/td[' + c + ']/a/@href'
#
#                 f = 'https://book.douban.com' + selector.xpath(url)[0]  #每个标签对应的子网站链接
#                 nums += 1   # 标签序号
#                 print(f,nums)
#                 html = requests.get(f, headers=headers)
#                 selector = etree.HTML(html.text)
#
#                 for d in range(1,21):
#                     d = str(d)
#
#                     url1 = '//*[@id="subject_list"]/ul/li[' + d + ']/div[2]/h2/a/@href'
#
#                     nnn = selector.xpath(url1)[0]
#
#                     #print(f, nums, nnn)
#
#
#             except IndexError:
#                 pass
#
#
# # for a in range(1,7):
# #     for b in range(1,10):
# #         for c in range(1,5):
# #
# #             try:
# #                 a = str(a)
# #                 b = str(b)
# #                 c = str(c)
# #                 bq = '//*[@id="content"]/div/div[1]/div[2]/div[' + a + ']/table/tbody/tr[' + b + ']/td[' + c + ']/a/text()' # 标签xpath位置
# #                 sl = '//*[@id="content"]/div/div[1]/div[2]/div[' + a + ']/table/tbody/tr[' + b + ']/td[' + c + ']/b/text()' # 标签中书量xpath位置
# #
# #                 label = selector.xpath(bq)[0] # 使用xpath对标签查询
# #                 sort = a
# #                 num = selector.xpath(sl)[0]
# #
# #
# #                 # cursor.execute("insert into c (label,sort,num) values(%s,%s,%s)", (label, sort, num))    # 获取数据插入数据库
# #                 # conn.commit()
# #
# #                 # 输出所查询信息
# #                 print(label, sort, num)
# #             except IndexError:
# #                 pass
#
#
#
