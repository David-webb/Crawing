# -*- coding:utf-8 -*-

import MySQLdb
import traceback
import datetime

class QuquMysqlOps():
    def __init__(self, host, userName, pwd, DbName):
        self.td = MySQLdb.connect(host, userName, pwd, DbName)
        self.cursor = self.td.cursor()
        pass

    def __del__(self):
        self.cursor.close()
        pass

    def createTables(self):
        sql = '''
        create table MenuItems(
            MID int,
            menuName varchar(100) primary key not null,
            mainPageUrl varchar(200) not null,
            nextPageUrl varchar(200),
            state int default 0,
            last_update_Date date,
            daliy_state default 0,
        )auto_increment = 1;
        '''

        sql2 = '''
        create table PaperInfo(
            PID varchar(100) primary key,
            ptitle varchar(200) not null,
            ChineseText text,
            EnglishText text,
            originText  text,
            purl  varchar(200),
            pType varchar(100),
            CONSTRAINT FK_ID FOREIGN KEY (pType) REFERENCES MenuItems(menuName)

        );
        '''
        try:
            self.cursor.execute(sql)
            self.td.commit()
        except:
            print '创建菜单表格失败！'
            print traceback.format_exc()
            return False

        try:
            self.cursor.execute(sql2)
            self.td.commit()
        except:
            self.td.rollback()
            print "创建文章信息表格失败！"
            print traceback.format_exc()
            return False
        return True
        pass


    def insertIntoTable(self, tableName, dataList, ROLLBACK=True):
        sql = ''
        if tableName == 'MenuItems':
            print dataList
            sql = 'INSERT IGNORE INTO MenuItems(MID, menuName, mainPageUrl, nextPageUrl) VALUE(%s,%s,%s,%s)'
        elif tableName == 'PaperInfo':
            sql = 'INSERT IGNORE INTO PaperInfo VALUE(%s,%s,%s,%s,%s,%s,%s,%s)'

        try:
            self.cursor.executemany(sql, dataList)
            if ROLLBACK:
                self.td.commit()
            self.td.commit()
        except:
            self.td.rollback()
            print '插入数据到表' + tableName + '出错！'
            print traceback.format_exc()
            return False
        return True


    def GetNextPageUrl(self, daliyUpdate=False):
        if daliyUpdate:
            today = datetime.date.today()
            sql = 'select * from MenuItems where last_update_Date < "' + str(today) + '" limit 1;'
        else:
            sql = 'select * from MenuItems where state = 0 limit 1'
        try:
            self.cursor.execute(sql)
        except:
            print '已经全部下载完！'
            # print traceback.format_exc()
            return False
        return self.cursor.fetchone()
        pass

    def daliyMenuUpdate(self, mDate, mID):
        sql = 'update MenuItems set last_update_Date = "' + str(mDate) + '" where MID=' + str(mID)
        print sql
        try:
            self.cursor.execute(sql)
            self.td.commit()
        except:
            print '每日更新菜单项出错！'
            print traceback.format_exc()
            self.td.rollback()
        pass

    def UpdateMenuItems(self, nextUrl, state, menuName):
        sql = 'update MenuItems set  nextPageUrl="' + nextUrl + '", state=' + str(state) + ' where menuName="' + menuName + '"'
        print sql
        try:
            self.cursor.execute(sql)
            self.td.commit()
            return True
        except:
            self.td.rollback()
            print '更新菜单项出错！'
            print traceback.format_exc()
            return False
            pass
        pass


if __name__ == '__main__':
    testObj = QuquMysqlOps('localhost', 'root', 'tw2016941017', 'ququDB')
    # 创建表格
    # testObj.createTables()

    # 测试输出
    # testObj.cursor.execute('select ChineseText from PaperInfo limit 1;')
    # tmpstr = testObj.cursor.fetchone()
    # print tmpstr[0]

    # 测试每日更新过程中获取下一页地址的函数
    # print testObj.GetNextPageUrl(True)

    # mysql编码测试
    # 测试1
    # sql = 'select ChineseText from PaperInfo where  PID=100000'
    # testObj.cursor.execute(sql)
    # CText = testObj.cursor.fetchone()[0]
    # mainPage = CText.decode('utf-8')
    # print mainPage
    # import chardet
    # print chardet.detect(mainPage)

    # 测试2
    # ChineseText = "这是测试！"
    # sql = 'insert into PaperInfo value(100000, "testPage","'+ChineseText.decode('utf-8').encode('GBK')+'","","","","国际","2016-7-27")'
    # testObj.cursor.execute(sql)
    # testObj.td.commit()


    # 测试4：从pycharm插入数据，并取出
    # sql1 = 'insert into MenuItems value(21,"测试类型2","www.baidu.com","", 1,"")'
    # testObj.cursor.execute(sql1)
    # testObj.td.commit()

    # 测试3: 从终端插入数据，从pycharm中获得条目来检测编码类型
    # sql = 'select * from MenuItems where MID>=20;'
    # testObj.cursor.execute(sql)
    # tmptuble = testObj.cursor.fetchall()
    # print tmptuble[0][1]
    # import chardet
    # print chardet.detect(tmptuble[1][1]), chardet.detect(tmptuble[0][1])
    # for i in tmptuble:
    #     print i[1]

    # import chardet
    # print chardet.detect(tmptuble[1])





    pass