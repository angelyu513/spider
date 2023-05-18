# 主程序
# 首先导入需要的模块
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
import jieba  # 通过jieba中文分词
import numpy as np
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image  # 更改图片需要Image模块

# 获取网页数据
def geturl(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    try:
        req = requests.get(url, headers=head)
        return req.text
    except:
        print('获得网页信息错误')

# 解析数据  我是用字典的方式来保存数据，最终用列表存储，因为用pandas库可以很好的自动把字典转为DateFrame，这样就直接可以保存成csv，excel等
def Parserdata(html):
    soup = BeautifulSoup(html, 'lxml') # 通过lxml进行解析网页
    itemtable = soup.find_all('table')
    databook = []
    for item in itemtable:
        datab = {}
        item = str(item)
        findlink = re.compile(r'<a class="nbg" href="(.*?)" onclick=')  # 详细链接
        Link = re.findall(findlink, item)
        datab['详细链接'] = Link[0]

        findimg = re.compile(r'<img src="(.*?)"')
        img = re.findall(findimg, item)
        datab['图片链接'] = img[0]

        findbookname = re.compile(r'<a href=.* title="(.*?)"', re.I)
        bookname = re.findall(findbookname, item)
        datab['书名'] = bookname[0]

        findauthor = re.compile(r'<p class="pl">(.*?)</p>')
        author = re.findall(findauthor, item)
        datab['作者'] = author[0]

        findsc = re.compile(r'<span class="rating_nums">(.*?)</span>')
        score = re.findall(findsc, item)
        datab['评分'] = score[0]

        findsuy = re.compile(r'<span class="inq">(.*?)</span>')
        summary = re.findall(findsuy, item)
        datab['概述'] = summary[0]
        databook.append(datab)
    return databook

# 以csv文件的形式保存到book文件夹c
def savepoint(data):
    # 判断D盘有没有book文件夹
    Jo = 'D:\\'
    if not os.path.exists(Jo + 'book'):
        os.mkdir(os.path.join(Jo, 'book'))
    else:
        print('文件夹已经存在，准备传入数据')
    df = pd.DataFrame(data)
    df.to_csv(Jo + 'book\\' + 'book.csv')

    # 如果保存成excel
    # df =pd.DataFrame(data)
    # df.pd.to_excel(Jo +'book\\' + 'book.xls')
# 如果要保存到mysql中
def savemysql(data):
    # 导入sqlalchemy库，进行mysql操作
    from sqlalchemy import create_engine
    engin = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/schooldb?charset=utf8')  # 连接mysql的方式
    mate = pd.read_csv("D:\\book\\book.csv", engine='python', encoding='utf-8')  # 读取csv文件或者Excel文件进行保存到mysql
    mate.to_sql('book', con=engin, if_exists='replace')  # 如果存在则替换

def getdata(num): #传入num参数 0为排行，1为详细链接，2图片链接,3书名,4作者,5评分,6概述
    import csv  # 导入csv模块
    with open(r'D:\book\book.csv', 'r', encoding='utf-8') as f:
        data1 = csv.reader(f)  # 通过csv模块中的reader来读取csv
        title = next(data1)   # data是一个迭代对象，通过next迭代第一行，因为第一行是标题不用取
        score = []
        for i in data1:
            score.append(i[num])
        return score
def analysescore():

    sc = {}
    for i in getdata(5):
        if i not in sc:
            sc[i] = 1
        else:
            sc[i] += 1
    plt.rcParams['font.sans-serif']=['SimHei']
    # 设置显示中文字体
    plt.rcParams['axes.unicode_minus']= False
    # 这样评分是无序的
    # for sc,num in sc.items():
    #     plt.bar(sc,num)
    # 根据列表索引完成排序
    su = sorted(sc.keys())
    Datanum = []
    for i in su:
        Datanum.append(sc[i])
    for i in range(len(su)):
        plt.bar(su[i], Datanum[i])
    plt.title('图书评分统计图')
    plt.xlabel('数量')
    plt.ylabel('评分')
    plt.show()

def analysemon():
    money = []
    for se in getdata(4):
        data=se.split(' / ')
        my = data[-1]
        money.append(my)
    moneys=[]
    for m in money:  # 去掉元这个字
        if m[-1] == '元':
            m = m.replace('元', '')
            moneys.append(m)
    for s in moneys:
        ime = str(s)    # 把59.00/49.00这样的数据 求平均值
        if len(ime) > 7:
            he = s.split('/')
            num = (float(he[0]) + float(he[1]))/2
            moneys.remove(s)
            moneys.append(num)
    for d in moneys:
        if float(d) < 1:    # 一本书价格一般不小于10，删除错误数据
            moneys.remove(d)
    mon = pd.DataFrame(moneys, dtype='float')
    # 通过pandas自带的值来查
    # print(mon.max())
    # print(mon.median())
    # print(mon.mean())
    # print(mon.min())
    # 也可以直接通过 describe获得所以信息
    print(mon.describe())  # 查书价钱的平均，最大等信息

def anyciyun():
    #词语
    a = ' '.join(getdata(6))
    duan_cut = jieba.cut(a)
    duan_text = ' '.join(duan_cut)
    # img图片做词云背景
    img = np.array(Image.open(r'D:\book\微信图片_2022070815.jpg'))
    word = WordCloud(background_color='white',\
                     width= 800,\
                     height=600,\
                     max_words= 200,
                     mask =img,\
                     contour_width= 4,\
                     contour_color= 'steelblue',\
                      font_path= r'D:\book\simsun.ttc'
                     ).generate(duan_text)
    #x写入到book文件夹中
    word.to_file(r'D:\book\booooo.jpg')
    #通过matplotlib展示出来
    fig = plt.figure(1)
    plt.imshow(word)
    plt.axis('off')
    plt.show()

def analysetime():
    times = []
    for he in getdata(4):  #找到出版时间
        data = he.split(' / ')
        my = data[-2]
        times.append(my)
    # 清洗数据
    ti = []
    # 分5年一段
    h = [0, 0, 0, 0, 0, 0]
    # 找到年的一段加入到ti列表里
    for i in times:
        s = i.split('-')
        ti.append(s[0])
    # 遍历时间，找到时间分布情况
    for i in ti:
        if 1990 < int(i) <= 1995:
            h[0] += 1
        elif 1995 < int(i) <= 2000:
            h[1] += 1
        elif 2000 < int(i) <= 2005:
            h[2] += 1
        elif 2005 < int(i) <= 2010:
            h[3] += 1
        elif 2010 < int(i) <= 2015:
            h[4] += 1
        else:
            h[5] += 1
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 设置显示中文字体
    plt.rcParams['axes.unicode_minus'] = False
    plt.title('出版时间分部情况')
    # 分布情况画饼状图
    lab = ['1990-1995', '1995-2000', '2000-2005', '2005-2010', '2010-2015', '2015年以上']
    plt.pie(h, labels=lab, autopct='%1.1f%%')  # 以百分之多少为单位
    plt.show()
