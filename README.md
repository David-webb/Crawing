# ���棺����Ӣ����
## ���漼����
> urllib + Beautiful soup\re + mysql
## ��Ҫ��
> ������������Ŀ�������������Ӣ�����ġ�
1. first_ququSpider �����re �� BS����ϰ��ָ��ȡ�˲������£���û�����ݿ�֧�֣�������ʵ��˵������ϸ�ڴ�������ע�ͣ����ﲻ��̸��
2. improving_ququspider �ǽ��׵����棬���������ݿ⣬�ҹ��ܡ��ṹ�������ƣ���֧�ֶ��ڸ��µĽű��������˵����������Ը���Ŀ��

### ����˵����
> 1. ����˵���Ҳ���������������µ�һ������
  2. ���շ����Ӧ�������е��ļ������浽���ݿ�
  3. ÿƪ���¶�Ҫ��һ��ID,���ڲ��أ����ID�����µ�url����ȡ
  4. ���ÿ���Զ�����ģ��:
	(1) Ϊ��MenuItem���һ���������ԣ���¼�ϴθ��µ�����;
	(2) �ӱ�MenuItem��ȡÿ��Item��mainPageUrl��Ȼ��һҳһҳ������ȡ���£�ֻ��ȡ�ϴθ������ں������;
	(3) �������������ԣ���ϵͳ��ǰ��ʱ����Ϊ����ֵ

### �ṹ��ƣ�
> 1. �洢
(1)�˵��Ĵ洢��MID���˵���(��������)��url����ҳ�����Ѿ����ص�ҳ����pageUrlPattern����������
	˵������Ҫע��˵���������ʱ��Ҫ����ȡ��һҳ����������url��

(2)�������ݵĴ洢��PID(PID������url����ȡ)�����ģ�Ӣ�ģ�ԭ�ģ�Purl��Type��MID��ţ�
	
  2. �˵���ʹ�ã�ÿ�δ�db�˵�����ѡȡһ��û������ѡ�����url,���ز�ժȡ�ļ���Ϣ�������ݿ⣬���²˵���


### ���ݿ���ƣ�mysql��
1. �˵���(MenuItems):
    sql = '''
   	create table MenuItems(
            MID int,
            menuName varchar(100) primary key not null,
            mainPageUrl varchar(200) not null,
            nextPageUrl varchar(200),	
            state int default 0
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


