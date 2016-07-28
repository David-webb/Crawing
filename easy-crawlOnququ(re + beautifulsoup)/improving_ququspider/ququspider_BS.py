# -*- coding:utf-8 -*-
# 声明编码方式 默认编码方式ASCII 参考https://www.python.org/dev/peps/pep-0263/
import urllib
import codecs
import re
from bs4 import BeautifulSoup
from ququDbOp import QuquMysqlOps
import datetime

'''
ququSpiderwithBS类：
    1. 功能：
        从蛐蛐英文网获得所有的文章的信息并保存，将每篇文章的中英文分开。
    2. 流程：
        读取菜单，解析每一类文章，提取文章内容，提取的同时实现中英文分离
'''


class ququSpiderwithBS():
    def __init__(self):
        self.basicUrl = 'http://www/qqenglish.com'
        self.dbObj = QuquMysqlOps('localhost', 'root', 'tw2016941017', 'ququDB')
        pass

    # 获得蛐蛐英文网首页的菜单url
    def getququMenu(self):
        page = urllib.urlopen('http://www.qqenglish.com').read()
        soup = BeautifulSoup(page, from_encoding='GBK')     # BeautifulSoup 会将文本全部转成Unicode,因为有编码自动检测
                                                            # print soup.prettify() 输出时默认编码是utf-8 (也可以设置成指定编码)
        menudict = {}
        basicUrl = 'http://www.qqenglish.com'
        indextmp = soup.find_all("div", id="menu")
        menuList = indextmp[0].find_all('a')                # 从网站主页提取所有的菜单项
        for i in menuList:
            menudict[i.string.encode('utf-8')] = basicUrl + i.get('href')
        del menudict['纽约时报中文网']                        # 将这两项删除是因为，其他所有的文章都是来源于这两家报社网站
        del menudict['华尔街日报中文网']
        # print menudict
        count = 1
        for i in menudict:                                  # 解析每个菜单项的主页，获取相关信息，在数据库中建立菜单表（MenuItems）
            print '正在解析" ' + i + ' "菜单项......'
            if self.getPaperUrlInfo(i, menudict[i], count, True) == False:
                print '程序出错，强制关闭！'
                return False
            count += 1

        # return menudict
        pass



    '''

        1. 获得某一页中所有文章的url
        2. 根据参数controlInfo判断是否需要解析页底信息
        3. 调用文章解析函数，将本页所有的文章的具体内容提取出来
    '''
    # 获得指定网页中所有保存有文章的网页的url
    def getPaperUrlInfo(self, menuName, pageUrl, mID, controlInfo=False):
        print '正在解析' + menuName + '指定页面...'
        page = urllib.urlopen(pageUrl).read()
        soup = BeautifulSoup(page, from_encoding='GBK')
        leftContainer = soup.find('div', id='leftN_title')
        objlist = leftContainer.div.contents
        tmplist = []
        for i in objlist:
            if i != '\n':
                tmplist.append(i)
        if len(tmplist) == 2:
            paperUrlList = tmplist[0].find_all('ul')        # 包含本页所有paper Url的tag
            conInfo = tmplist[1]                            # 包含下一页url的tag
        else:
            print '结构解析出现偏差！'
            return False

        # 首先插入菜单项
        if controlInfo == True:
            if self.dbObj.insertIntoTable('MenuItems', [[mID, menuName, pageUrl, self.getNextPageUrl(conInfo)]]):
                print '菜单项插入成功！'
            else:
                print '菜单项插入错误！'
                return False

        # 解析当前页的所有文章的url
        basicUrl = 'http://www.qqenglish.com'
        for i in paperUrlList:
            purl = basicUrl + i.li.a['href']
            ptitle = i.li.a.string.encode('utf-8')
            pID = i.li.a['href'].split('/')[-1].split('.')[0]
            if self.parsePapers(purl, ptitle, pID, menuName) == False:
                return False

        # 更新已有菜单项
        if controlInfo == False:
            nextUrl = self.getNextPageUrl(conInfo)
            state = 0
            if nextUrl == '':        # 没有下一页了
                state = 1
            return self.dbObj.UpdateMenuItems(nextUrl, state, menuName)

        pass

    def getNextPageUrl(self, conInfoTag):
        basicUrl = 'http://www.qqenglish.com'
        nextUrlTag = conInfoTag.div.find('a', text="下一页")
        if nextUrlTag:
            nextPageUerl = basicUrl + nextUrlTag['href']
            return nextPageUerl
        else:
            print '没有下一页了！'
            return ''
        pass


    '''
        从某一新闻页提取文章信息，并以中文、英文、原文的方式保存
    '''
    def parsePapers(self, purl, ptitle, PID, menuName, Date=''):
        print '正在解析' + purl + '指定文章......'
        ChineseText = ''
        EnglishText = ''
        originText = ''
        page = urllib.urlopen(purl).read()
        soup = BeautifulSoup(page, from_encoding='GBK')
        # soup = soup.encode('utf-8')
        try:
            content = soup.find('div', class_="content")
            paraList = content.find_all('p')
        except AttributeError:
            print '无法解析的页面，自动跳过！'
            return True

        for i in paraList:
            if i.string != None:
                if self.IsChineseCharIn(i.string):
                    ChineseText += (i.string + '\n')
                else:
                    EnglishText += (i.string + '\n')
                originText += i.string
        dataList = [[PID, ptitle, ChineseText.encode('utf-8'), EnglishText.encode('utf-8'), originText.encode('utf-8'), purl, menuName, Date]]
        if Date == '':
            return self.dbObj.insertIntoTable('PaperInfo', dataList)
        else:
            return self.dbObj.insertIntoTable('PaperInfo', dataList, False)

        pass

    def IsChineseCharIn(self, strObj):
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        #一个小应用，判断一段文本中是否包含简体中：
        match = zhPattern.search(strObj)
        if match:
            return True
        else:
            return False


    def mainSpider(self):
        nextItem = self.dbObj.GetNextPageUrl()
        while(nextItem):
            MID = nextItem[0]
            menuName = nextItem[1]
            nextUrl = nextItem[3]
            self.getPaperUrlInfo(menuName, nextUrl, MID)
            # break
            nextItem = self.dbObj.GetNextPageUrl()
            pass
        pass



if __name__ == '__main__':
    tmpObj = ququSpiderwithBS()
    # tmpObj.getququMenu()
    tmpObj.mainSpider()
    # tmpObj.getControlInfo('http://www.qqenglish.com/bn/bn/', 1, True)
    # tmpObj.parsePapers('http://www.qqenglish.com/bn/20038.htm','','','')