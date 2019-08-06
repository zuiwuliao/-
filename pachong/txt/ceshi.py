

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


# 小说标签
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
            txt_biaoqian_url = 'https://www.80txt.com' + selector.xpath(txt_biaoqian_urls)[0][:-6]   # 标签url    [0]代表符合此条件的第一个结果    [:-x]代表从末尾删除x个字符
            pindao = 1
            nums += 1  # 目前标签序号
            print(pindao, nums, txt_biaoqian_name)

            get_txt_biaoqian_label(nums, txt_biaoqian_url)  # 传递小说标签编号，小说标签列表样式

        except IndexError:
            pass

    for a in range(1, 30, 2):
        try:
            a = str(a)
            txt_biaoqian_names = '//*[@id="nav"]/ul/li[' + a + ']/a/@title'  # 标签页名字样式
            txt_biaoqian_urls = '//*[@id="nav"]/ul/li[' + a + ']/a/@href'  # 标签页url样式
            txt_biaoqian_name = selector.xpath(txt_biaoqian_names)[1]  # 标签名字
            txt_biaoqian_url = 'https://www.80txt.com' + selector.xpath(txt_biaoqian_urls)[1][:-6]  # 标签url
            pindao = 2
            nums += 1  # 目前标签序号
            print(pindao, nums, txt_biaoqian_name)

            get_txt_biaoqian_label(nums, txt_biaoqian_url)  # 传递小说标签编号，小说标签列表样式

        except IndexError:
            pass


# 每个小说标签的列表页链接
def get_txt_biaoqian_label(nums, txt_biaoqian_url):
    try:
        for a in range(1, 31):
            a = str(a)
            url = txt_biaoqian_url + a + '.html'
            print(url)
            get_txt_biaoqian_xiangqing(nums, url)   # 传递小说标签编号，小说标签列表url
    except IndexError:
        pass


# 小说标签详情
def get_txt_biaoqian_xiangqing(nums, url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    # print(selector)
    try:
        urls = '//*[@id="list_art_2013"]/div[1]/div[1]/div[1]/a/@href'  # 小说url
        title = '//*[@id="list_art_2013"]/div[1]/div[1]/div[1]/a/text()'    # 小说名字
        for a in range(0, 20):  # a 代表选择第0到第10个标签，总共20个
            txt_url = selector.xpath(urls)[a]
            txt_title = selector.xpath(title)[a]
            print(txt_url, txt_title)

            get_txt_xiangiqng(nums, txt_url)


    except IndexError:
        pass


# 小说信息
def get_txt_xiangiqng(nums, txt_url):
    html = requests.get(txt_url, headers=headers)

    html1 = html.content # 解压网页gzip
    # print(html1.decode('utf-8'))   # 输出网页修改为utf-8格式
    selector = etree.HTML(html1)
    # selector = etree.HTML(html.text)
    try:
        txt_id = re.findall('\d+', txt_url)[1]  # 小说id
        txt_img = selector.xpath('//*[@id="soft_info_para"]/div[2]/img/@src')[0]
        txt_title = selector.xpath('//*[@id="soft_info_para"]/h1/text()')[0][:-7]   # 小说名
        txt_author = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[1]/a/text()')[0]   # 作者
        txt_daxiao = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[2]/text()')[0]   # 大小
        txt_dianji1 = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[3]/text()')[0][:-2]   # 日点击
        txt_dianji2 = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[4]/text()')[0][:-2]   # 周点击
        txt_dianji3 = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[5]/text()')[0][:-2]   # 月点击
        txt_dianji4 = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[6]/text()')[0][:-2]   # 总点击
        txt_jindu = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[7]/strong/text()')[0]   # 进度
        txt_gx_time = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[8]/text()')[0]   # 更新时间
        txt_gx_zhangjie = selector.xpath('//*[@id="soft_info_para"]/div[2]/li[10]/text()')[0]   # 最新章节
        txt_down1 = 'https://dt.80txt.com/' + txt_id + '/' + txt_title + '.txt' # 主下载链接
        txt_down2 = 'https://txt.80txt.com/' + txt_id + '/' + txt_title + '.txt' # 备用下载链接
        txt_jj = selector.xpath('//*[@id="mainSoftIntro"]/p/text()')[6] # 电子书简介


        # print(selector)
        # print(html1.decode('utf-8'))
        print(txt_id, nums)
        print(txt_id, txt_img, txt_title, txt_author, txt_daxiao, txt_dianji1, txt_dianji2, txt_dianji3, txt_dianji4, txt_jindu, txt_gx_time, txt_gx_zhangjie, txt_down1, txt_down2, txt_jj)

        # cursor.execute("insert IGNORE into txt_bq (txt_id,nums) values(%s,%s)", (txt_id, nums))
        # cursor.execute("insert IGNORE into txt_xq (txt_id,txt_img,txt_title,txt_author,txt_daxiao,txt_dianji1,txt_dianji2,txt_dianji3,txt_dianji4,txt_jindu,txt_gx_time,txt_gx_zhangjie,txt_down1,txt_down2,txt_jj) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (txt_id, txt_img, txt_title, txt_author, txt_daxiao, txt_dianji1, txt_dianji2, txt_dianji3, txt_dianji4, txt_jindu, txt_gx_time, txt_gx_zhangjie, txt_down1, txt_down2, txt_jj))
        # conn.commit()
        # time.sleep(1)

    except IndexError:
        # pass
        print('cuo')




if __name__ == '__main__':
    urls = 'https://www.80txt.com/'  # 八零电子书首页
    get_txt_biaoqian(urls)