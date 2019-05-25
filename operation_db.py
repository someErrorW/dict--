"""
dict项目用于处理数据
"""

import pymysql
import hashlib
import time


# 编写功能类 提供给服务端使用
class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 database='ele_dict',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.chartset = charset
        self.connect()  # 连接数据库

    def connect(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.chartset)  # 这里需要键值传参

    # 产生游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()

    # 处理查单词
    def query(self, word):
        sql = "select mean from words where word = '%s';" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]
        else:
            return False

    # 处理登录
    def login(self, name, passwd):
        sql = "select * from user where name = %s and passwd = %s;"

        # 加密处理
        hash = hashlib.md5((name + 'the-salt').encode())
        hash.update(passwd.encode())
        self.cur.execute(sql, [name, hash.hexdigest()])  # 执行sql语句
        if self.cur.fetchone():
            # 如果找到，说明用户密码在数据库中存在，允许登录
            return True
        else:
            return False

    # 处理注册
    def register(self, name, passwd):
        sql = "select * from user where name = '%s'" % name
        # select不需要commit
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 如果查询到结果
        if r:
            return False

        # 加密处理
        hash = hashlib.md5((name + 'the-salt').encode())
        hash.update(passwd.encode())
        sql = "insert into user (name,passwd) values (%s,%s);"

        try:
            self.cur.execute(sql, [name, hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    # 插入历史记录
    def insert_history(self, name, word):
        tm = time.ctime()
        sql = "insert into hist (name,word,time) values (%s,%s,%s);"
        try:
            self.cur.execute(sql, [name, word, tm])
            self.db.commit()
        except Exception:
            self.db.rollback()

    # 历史记录
    def history(self, name):
        sql = "select name,word,time from hist where name='%s' order by id desc limit 10;" % name

        self.cur.execute(sql)

        return self.cur.fetchall()
