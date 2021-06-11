# -*- codeing = utf-8 -*-
# @Time : 2020-12-02 23:07
# @Author : fancyicookie
# @File : test1.py
# @Software : PyCharm

# def main(a):
#     print("diaoyong", a)
# main(2)
#
# if __name__ == "__main__":#当程序执行时
# #调用函数
#     main(1)     #在这儿写main比较好控制之后如果函数比较多了，函数的执行顺序。

# control+? 可以整行注释掉！！！

# 引入系统模块
import sys
import os

# 引入自定义模块
# 假设自己写一个函数t1.py在test中，然后from test import t1

#引入第三方模块（最常用）
import re






#这是我测试的第一个python程序
#print("hello,world")

#这是单行注释
'''
这是第一行注释
这是第二行注释

'''
print("python")

a = 10
print("这是变量:", a)

baseurl = "http://start"
for i in range(0,10):
    url = baseurl + str(i)
    url2 = url +".psp"
    print(url2)

    baseurl = "http://www.cuc.edu.cn/news/1901/list"
    for i in range(1,51):          #调用获取页面信息的函数50次，range后左闭右开
        url = baseurl + str(i)      #疑问：可能是页面的循环不太懂，为什么写个str+循环，豆瓣就可以爬取多个页面，中传却不可以。
        url = url +".psp"
        print("第%d页" %(i))
        print(url)
        #html = askURL(url)