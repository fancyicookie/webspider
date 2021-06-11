# -*- codeing = utf-8 -*-
# @Time : 2020-12-02 23:04
# @Author : fancyicookie
# @File : spider.py
# @Software : PyCharm

#没有调用过就显示是灰色的
# import xlwt     #进行excel操作
# import sqlite3   #进行SQLite数据库操作
from bs4 import BeautifulSoup     #网页解析
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error    #指定URL，获取网页数据
import xlwt

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣电影top250.xls"
    #3.保存数据
    saveData(datalist,savepath)
    # askURL("https://movie.douban.com/top250?start=0")

#影片详情连接的规则
findLink = re.compile(r'<a href="(.*?)">')   #创建正则表达式对象，表示规则（字符串的模式）
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  #re.S忽略换行的情况，让换行符包含在字符中。
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

#1.爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):          #调用获取页面信息的函数25次，range后左闭右开
        url = baseurl + str(i*25)  #难道这个只针对特定的页面吗？
        html = askURL(url)
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")  #html解析器
        for item in soup.find_all('div', class_="item"):   #查找符合要求的字符串，形成列表,class要有下划线表示class属性，属性下面有item
            # print(item)  #测试：查看电影item的全部信息
            data = [] #保存一步电影的所有信息
            item = str(item)
            # print(item)
            # break
            # 影片详情的连接
            link = re.findall(findLink,item)[0]        #re库用来通过正则表达式查找指定的字符串，弹幕说此处[0]代表文本
            data.append(link)                          #添加链接

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)                        #添加图片

            titles = re.findall(findTitle,item)       #片名有中文名也有外文名等等，有的只有中文，没有外文
            if(len(titles) == 2):
                ctitle = titles[0]                     #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")     #去掉无关符号
                otitle = re.sub('\xa0', " ", otitle)
                data.append(otitle)                    #添加外国名
            else:
                data.append(titles[0])
                data.append(' ')                  #外文名留空

            rating = re.findall(findRating,item)[0]
            data.append(rating)                        #添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)                      #添加评价人数

            inq = re.findall(findInq,item)           #这个地方后面加[0]就只能打印出评价的第一个字。
            if len(inq) != 0:
                inq = inq[0].replace("。","")           #去掉句号
                data.append(inq)                        #添加概述
            else:
                data.append(" ")
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)  #去掉<br/>
            bd = re.sub('/'," ",bd)    #替换/
            bd = re.sub('\xa0'," ",bd)
            data.append(bd.strip())    #去掉前后的空格
            datalist.append(data)     #处理好的一部电影信息放入datalist

    return datalist

# 得到指定一个URL的网页内容
def askURL(url):              #模拟浏览器头部信息系，向豆瓣服务器发送消息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }  # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接受什么水平的文件内容）


    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
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
    sheet = book.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)     #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外文名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])       #列名 ；sheet.write(0,i,col[i])写入数据，第一个参数“行”，第二个参数“列”，第三个参数内容
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])   #数据

    book.save(savepath)          #保存数据表
if __name__ == "__main__":            #当程序执行时，调用函数
    main()
    print("爬取完毕!")