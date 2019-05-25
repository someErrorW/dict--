"""
    将单词表插入数据库中
"""

import pymysql
import re

f = open('dict.txt')  # 默认读权限

# 链接数据库
db = pymysql.connect(host='localhost',
                     user='root',
                     passwd='123456',
                     database='ele_dict',
                     charset='utf8')
cur = db.cursor()  # 创建游标对象

sql = 'insert into words (word,mean) values(%s,%s);'

for line in f:
    # 正则匹配
    tup = re.findall(r'(\w+)\s+(.*)', line)[0]
    try:
        cur.execute(sql, tup)
        db.commit()
    except Exception:
        db.rollback()

# 关闭文件
f.close()
cur.close()
db.close()
