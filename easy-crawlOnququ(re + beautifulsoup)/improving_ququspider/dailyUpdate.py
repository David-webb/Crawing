# -*- coding:utf-8 -*-

from ququspider_BS import ququSpiderwithBS
from ququDbOp import QuquMysqlOps
import urllib
import datetime
from bs4 import BeautifulSoup

class daliyUpdate():
    def __init__(self):
        self.td = QuquMysqlOps('localhost', 'root', 'tw2016941017', 'ququDB')
        self.qSpider = ququSpiderwithBS()
        pass

    # 获得指定网页中所有保存有文章的网页的url
    def getPaperUrlInfo(self, menuName, pageUrl, mID, Date):
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


        # 解析当前页的所有文章的url
        basicUrl = 'http://www.qqenglish.com'
        overFlag = False
        for i in paperUrlList:
            # pDate = time.strptime(i.li.span.string, '%Y-%m-%d')
            pDate = datetime.datetime.strptime(i.li.span.string, '%Y-%m-%d').date()
            if pDate > Date:                    # 如果文章的时间要晚于上次更新数据库的时间
                purl = basicUrl + i.li.a['href']
                ptitle = i.li.a.string.encode('utf-8')
                pID = i.li.a['href'].split('/')[-1].split('.')[0]
                if self.qSpider.parsePapers(purl, ptitle, pID, menuName, pDate) == False:
                    return False
            else:
                overFlag = True
                break

        if overFlag == False:
            nextUrl = self.qSpider.getNextPageUrl(conInfo)
            if nextUrl != '':
                self.getPaperUrlInfo(menuName, nextUrl, mID, Date)      # 递归调用
        else:
            today = datetime.date.today()
            # 更新菜单项日期
            self.td.daliyMenuUpdate(today, mID)
        return True

    def UpdateProcess(self):
        mitem = self.td.GetNextPageUrl(daliyUpdate=True)
        while(mitem):
            print mitem
            mID = mitem[0]
            menuName = mitem[1]
            mainPageUrl = mitem[2]
            mDate = mitem[5]
            # print type(mDate)
            if self.getPaperUrlInfo(menuName, mainPageUrl, mID, mDate)==False:
                print '解析出错！终止程序！'
                return False
            mitem = self.td.GetNextPageUrl(daliyUpdate=True)
            pass

        pass

    pass

if __name__ == '__main__':
    # 测试时间类型的比较方法
    # t = time.strptime('2016-7-20', '%Y-%m-%d')
    # t1 = time.strptime('2016-7-21', '%Y-%m-%d')
    # print type(t)
    # print t<t1
    tmpObj = daliyUpdate()
    tmpObj.UpdateProcess()
    #
    pass