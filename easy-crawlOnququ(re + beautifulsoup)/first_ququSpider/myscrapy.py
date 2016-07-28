# coding=utf-8
# 声明编码方式 默认编码方式ASCII 参考https://www.python.org/dev/peps/pep-0263/
'''
    本章代码主要功能：获取“蛐蛐英文网”的部分文章网页的源码并保存到本地文件
    使用到的技术： 正则表达式 和 Beautiful Soup，由于是初学，用正则表达式为主，后接触BS，遂用来代替了部分re（re易出错，可读性不好）
    功能实现步骤：
        1. 获取蛐蛐英文网的首页源码，并从中提取出菜单项及链接(保存到本地)
        2. 从各菜单项对应的主页获取网页获取相关文章的url并保存到本地文件
        3. 从保存url的文件中依次提取url,并获取对应页面的源码保存本地
'''


import urllib
import time
import re
import os
from bs4 import BeautifulSoup
from processIng import myencode
import codecs

# 获得蛐蛐英文网首页的菜单url
def getququMenu():
    with codecs.open("ququenglish.txt", 'r', encoding='utf-8') as mf:
        page = mf.read()
    soup = BeautifulSoup(page)
    menudict = {}
    indextmp = soup.find_all("div", id="menu")
    patt = u'<li><a href="(.*?)">(.*?)</a></li>'
    menurl = re.compile(patt, re.S | re.M)
    menulist = menurl.findall(myencode(str(indextmp[0])))
    for i in menulist:
         menudict[i[1]] = i[0]
    return menudict


# 获取蛐蛐英文网菜单中某一类（例如：文化）文章的主页，保存到本地
def getURLoftagetpage():
    temp = u"http://www.qqenglish.com"
    mdic =getququMenu()
    name = "Culture.txt"
    tpage = urllib.urlopen(temp + mdic[u'文化']).read()
    # print tpage
    with codecs.open(name, 'w', encoding='utf-8') as wr:
        wr.write(myencode(tpage))
    return name


# page = urllib.urlopen(temp).read()
# import codecs
# with codecs.open("ququenglish.txt", 'w', encoding='utf-8') as mf:
#     mf.write(myencode(page))

# print soup

# soup2 = BeautifulSoup(str(indextmp))
# menurlist = soup2.ul.children
# for i in menurlist:
#     if i is not '\n':
#         print i
#         # menudict[i.string] = i.a.get('href')
# print menudict



# print indextmp[0]

# print indextmp


# 获得指定网页中所有保存有文章的网页的url
def getpaperurls(page):
    soup = BeautifulSoup(page)
    mtmp = soup.find_all('div', id="leftMainContainer")
    soup2 = BeautifulSoup(str(mtmp))
    mtmp2 = soup2.find_all('ul')
    patt = u'href="(.*?)"'
    regeturl = re.compile(patt)
    with codecs.open('qqtranslation_url2.txt', 'w', encoding='utf-8') as fileurl:
        temp = u"http://www.qqenglish.com"
        for i in mtmp2:
            obj = regeturl.findall(str(i))[0]
            fileurl.write(temp+obj+u'\n')

    #
    # remodule = u'<div id="Container">.*<div id="list">.*<ul>(.*?)</ul>.*?<div>'
    # wurl = re.compile(remodule, re.M | re.S)
    # mlist = wurl.findall(page)
    # remodule2 = u'<a class="" href=(".*?") title=".+?" target="_blank">'
    # remodule3 = u'<a class="" href="(.*?)"'
    # urllist = []
    # for i in mlist:
    #     # print i
    #     wurl = re.compile(remodule2)
    #     mlist = wurl.findall(str(i))
    #     urllist.extend(mlist)
    # urllist2 = []  # 存放所有文章的url
    # for i in urllist:
    #     # print i
    #     wurl = re.compile(remodule3)
    #     mlist = wurl.findall(str(i))
    #     urllist2.extend(mlist)
    # # import pprint
    # # pprint.pprint(urllist2)
    # # print len(urllist2)
    #
    # temp = u"http://www.qqenglish.com"
    # with codecs.open('qqtranslation_url2.txt', 'w', encoding='utf-8') as fileurl:
    #     for i in urllist2:
    #         fileurl.write(temp+i+u'\n')


if __name__ == '__main__':
    name = getURLoftagetpage()
    with codecs.open(name, 'r', encoding='utf-8') as rd:
        page = rd.read()

    getpaperurls(page)

    with codecs.open('qqtranslation_url2.txt', 'r', encoding='utf-8') as rd:
        count = 80
        while(count < 120):
            count += 1
            turl = rd.readline()
            with codecs.open('./htmlSourcePage/thtml' + str(count) + '.txt', 'w', encoding='utf-8') as rd2:
                rd2.write(myencode(urllib.urlopen(turl).read()))

