# coding=utf-8
'''
    本章代码主要功能：将myscrapy.py保存的网页源码作为输入，提取出文章内容并保存到本地
    使用的技术： BS 和 正则表达式（前者为主， 后者多被注释掉了）， 网页编码转换（chardet模块）
'''

import urllib,  urllib2
import time
import re
import os
import codecs
import chardet

from bs4 import BeautifulSoup


# 获得网页源码
def getpage(mUrl):
    return urllib.urlopen(mUrl).read()
    pass

def Is_P_and_not_null(tag):
    return ( tag.name == 'p' )


# 从某一网页中抽取出文章（给出了bs和re两种提取方法，后者为注释部分）
def bs4Process(tmp, count):
    soup = BeautifulSoup(tmp)
    buffofnews = soup.find_all('div', class_="content")
    soup2 = BeautifulSoup(str(buffofnews))
    plist = soup2.find_all(Is_P_and_not_null)
    # print plist
    with codecs.open("./mhtmls/thtml" + count + ".txt", 'w', encoding='utf-8') as filecontainer:
        for i in plist:
            if i.string not in ['[', '', None]:
                filecontainer.write(i.string+'\n')
            # print str(myencode(i.string))
            # filecontainer.write(i.string)
    # pattern = u"<p>(.*?)</p>"
    # getptmp = re.compile(pattern, re.S | re.M)
    # buff = getptmp.findall(str(buffofnews))
    # print myencode(str(buff))
    # with codecs.open("./mhtmls/thtml3.txt", 'a') as filecontainer:
    #     for i in tmplist:
    #         if 'div' not in i:
    #             print i
    #             # filecontainer.write(i)

    # print tmplist
    pass



# 更改对象的编码为utf-8
def myencode(tmp):
    mychar = chardet.detect(tmp)
    bianma = mychar['encoding']
    print "编码格式：" + bianma + '\n'
    # return tmp.decode(bianma.lower(), 'ignore').encode('utf-8').decode('utf-8')
    html_1 = ''
    if bianma == 'utf-8' or bianma == 'UTF-8':
        html_1 = tmp
        # pass
        # html_1 = tmp.decode('utf-8', 'ignore').encode('utf-8')
    elif bianma == 'gbk' or bianma == 'GBK' :
        html_1 = tmp.decode('gbk', 'ignore').encode('utf-8')
    elif bianma == 'gb2312' or bianma == 'GB2312':
        html_1 = tmp.decode('gb2312', 'ignore').encode('utf-8')
    elif bianma == 'ascii' or bianma == 'ASCII':
        html_1 = tmp.decode('ascii', 'ignore').encode('utf-8')
    else:
        print "新格式！"
    return html_1.decode('utf-8')


def processWordpage(tmp):
    rem1 = u'<div class="content">.*?<div class="content">(<p>.+?</p>).*?</div>'
    r1 = re.compile(rem1, re.M | re.S)
    # tmp.decode('utf-8')
    # tmp.encode('utf-8')
    # print tmp)
    plist = r1.findall(tmp)
    print plist
    pass



# 调用bs４process进行循环抽取操作
def keeProcess(startnum, totalnum):
    count = startnum
    while(count < totalnum + startnum):
        count += 1
        with codecs.open("thtml" + str(count) + ".txt", 'r') as filecase:
            tmp = filecase.read()
            bs4Process(tmp, str(count))
    # processWordpage(tmp)


# with codecs.open('qqtranslation_url.txt', 'r', encoding='utf-8') as fileurl:
#     # print urllib.urlopen('http://www.baidu.com')
#     count = 0
#     for i in fileurl.readlines():
#         if count < 80:
#             print i
#             count += 1
#             tmp = getpage(i)
#             tmp = myencode(tmp)
#             with codecs.open('thtml'+str(count)+'.txt', 'w', encoding='utf-8') as filehtml:
#                 filehtml.write(tmp)
#                 # processWordpage(tmp)
#
#     # pass


if __name__ == '__main__':
    with codecs.open("latlon.txt", "r") as rf:
        tmp = rf.read()
        tmp = str(tmp).replace('"', "")
        tmp = str(tmp).replace("&quot;", '"')
        print tmp
        # import json
        # mdic = dict(tmp)
        # mlist = json.loads(myencode(tmp))
        # mlsit = pickle.loads(tmp)

    # keeProcess(80, 40)
