# 爬虫：蛐蛐英文网

## 爬虫技术：
> urllib + Beautiful soup\re + mysql 

## 概要：
> 这里有两个项目，都是针对蛐蛐英文网的。
> 1. first_ququSpider 是针对re 和 BS的练习，指爬取了部分文章，且没有数据库支持，其具体的实现说明的详细在代码中有注释，这里不具谈
> 2. improving_ququspider 是进阶的爬虫，加入了数据库，且功能、结构更加完善，还支持定期更新的脚本。下面的说明都是是针对该项目的

### 功能说明：
1. 保存菜单：也就是蛐蛐网对文章的一个分类
2. 按照分类对应下载所有的文件并保存到数据库
3. 每篇文章都要有一个ID,用于查重，这个ID从文章的url中提取
4. 设计每天自动更新模块:
   * (1). 为表MenuItem添加一个日期属性，记录上次更新的日期;
   * (2). 从表MenuItem提取每个Item的mainPageUrl，然后一页一页往下提取文章，只提取上次更新日期后的文章;
   * (3). 最后更新日期属性：用系统当前的时间作为更新值

### 结构设计：
1. 存储
+ 菜单的存储：MID：菜单项名称：菜单项主页url：下一页的URL：state：last_update_Date 
   * 说明：
   * (1). 要注意菜单表在生成时需要先爬取第一页的所有文章url
   * (2). “下一页的URL”和state两个字段是在构建数据库初次下载时用到的，前者在本菜单项对应的文章下载完成前，总是指向下一页，否则为空，state初始化为0，下载完后设置为1
   * (3). "last_update_Date",指示上次更新的时间，用于为定期功能模块的实现提供更新依据（更新该日期之后的文章）
+ 文章内容的存储：PID(PID从文章url中提取)：title: 中文：英文：原文：Purl：Type（menu菜单项）: paperDate

### 数据库设计（mysql）

1. 菜单表(MenuItems):

	sql = '''
   	    create table MenuItems(
            	MID int,
            	menuName varchar(100) primary key not null,
            	mainPageUrl varchar(200) not null,
            	nextPageUrl varchar(200),	
            	state int default 0
            )auto_increment = 1;
        '''
        
2. 文章表(PaperInfo):

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


