# -*- codeing = utf-8 -*-
# @Time : 2020-12-02 23:11
# @Author : fancyicookie
# @File : cuc_spider.py
# @Software : PyCharm

from bs4 import BeautifulSoup     #网页解析
import re       #正则表达式，进行文字匹配
import urllib.request, urllib.error    #指定URL，获取网页数据
import xlwt     #进行excel操作
import sqlite3   #进行SQLite数据库操作

def main():
    baseurl = "http://www.cuc.edu.cn/news/1901/list"
    #1.爬取网页
    datalist = getData(baseurl)
    #3.保存数据
    savepath = ".\\CUCnews.xls"
    saveData(datalist,savepath)

    # askURL("http://www.cuc.edu.cn/news/1901/list1.psp")
    # findLink = re.compile(r'<a href="(.*?)" target="_blank">')   #创建正则表达式对象，表示规则（字符串的模式）

#新闻详情连接的规则
findLink = re.compile(r'<a href="(.*?)" target="_blank">')   #创建正则表达式对象，表示规则（字符串的模式）
#新闻标题
findTitle = re.compile(r'<a href=.*? target="_blank">(.*?)</a>',re.S)
#新闻简介
findContent = re.compile(r'<div class="g-lastu">(.*)<p class="source">',re.S)
#新闻来源
findSrc = re.compile(r'<p class="source">(.*)<span class="mr10 ml10">')
#新闻日期
findDate = re.compile(r'</span>(.*)</p>')


#1.爬取网页
def getData(baseurl):
    datalist = []                 #定义datalist为一个列表
    for i in range(1,51):          #调用获取页面信息的函数50次，range后左闭右开
        url = baseurl + str(i)      #疑问：可能是页面的循环不太懂，为什么写个str+循环，豆瓣就可以爬取多个页面，中传却不可以。
        url = url +".psp"
        html = askURL(url)         #保存获取到的网页源码
    # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")  #html解析器
        for news in soup.find_all('ul', class_="news-list g-line"):   #查找符合要求的字符串，形成列表,class要有下划线表示class属性，属性下面有item
            #print(news)  #测试：查看news的全部信息
            data = [] #保存一条新闻的所有信息
            news = str(news)
            #
            link = re.findall(findLink,news)[0]   #re库用来通过正则表达式查找指定的字符串，弹幕说此处[0]代表文本
            data.append(link)                     #添加链接
            #print(link)

            Title = re.findall(findTitle,news)[0]
            data.append(Title)                    #添加标题
            #print(Title)

            Content = re.findall(findContent,news)[0]
            Content = Content.strip()             #去掉内容前后的空格
            data.append(Content)                  #添加新闻简介
            #print(Content)

            Src = re.findall(findSrc,news)[0]
            data.append(Src)                      #添加新闻来源
            #print(Src)

            Date = re.findall(findDate,news)[0]
            data.append(Date)                      #添加新闻日期

            datalist.append(data)                #把处理好的一条新闻放入datalist
    print(datalist)
    return datalist

# 得到指定一个URL的网页内容
def askURL(url):
    head = {           #模拟浏览器头部信息系，向豆瓣服务器发送消息
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
     }  # 用户代理，表示告诉CUC服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接受什么水平的文件内容）

    request = urllib.request.Request(url)   #CUC的网没有头部也没关系，本来就让你爬取，哈哈哈。
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:      #如果浏览器出现异常
        if hasattr(e,"code"):          #将这个错误捕获一下，打印出code以及reason
            print(e,code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


#保存数据
def saveData(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)   #创建workbook对象(文件）
    sheet = book.add_sheet('中传要闻',cell_overwrite_ok=True)     #创建工作表
    col = ("新闻详情链接","新闻标题","新闻简介","新闻来源","新闻日期")
    for i in range(0,5):
        sheet.write(0,i,col[i])       #列名 ；sheet.write(0,i,col[i])写入数据，第一个参数“行”，第二个参数“列”，第三个参数内容
    for i in range(0,300):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,5):
            sheet.write(i+1,j,data[j])   #数据

    book.save(savepath)          #保存数据表


if __name__ == "__main__":    #当程序执行时，调用函数
    main()
    print("爬取完毕!")