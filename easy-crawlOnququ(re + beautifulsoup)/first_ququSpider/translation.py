# coding=utf-8

'''
    将先前保存到本地的网页文章进行中英文分离，并分别保存到Chinese.txt 和 English.txt文件中
'''

__author__ = 'Tengwei'

import re
import codecs
from string import *
# from processIng import myencode


# 统计文件文字个数
def countwordnum(name):
    with codecs.open(name, 'r', encoding='utf-8') as chinesefile:
        print len(re.split(' |\n|\r|\s', chinesefile.read()))
        # wordList = split(countWords)
        # print len(countWords)


# 将若干篇文章中的中英文分离，并分别输出到Chinese.txt和English.txt

def seperation(startnum, totalnum):
    b = re.compile(u"[\u4e00-\u9fa5].*[！？。”]")
    d = re.compile(u"[a-zA-Z1-9][^\u4e00-\u9fa5]*[!?.]")   # 会将中文里面的英文也给找出来？？？
    count = 0
    while(count < totalnum):
        count += 1
        with codecs.open("./mhtmls/thtml" + str(count) + ".txt", 'r') as f:
            words = f.read().decode('utf-8')
            c = b.findall(words)
            e = d.findall(words)
            with codecs.open('Chinese.txt', 'a', encoding='utf-8') as wr:
                for i in c:
                    wr.write(i+'\n')
                wr.write('\n\n\n\n')
            with codecs.open('English.txt', 'a', encoding='utf-8') as wr1:
                for j in e:
                    if len(j) > 30:
                        wr1.write(j+'\n')
                wr1.write('\n\n\n')

if __name__ == '__main__':
    seperation(0, 120)
    countwordnum("English.txt")
    countwordnum("Chinese.txt")