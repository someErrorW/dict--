import os
import pymysql
import re

db = pymysql.connect(host = 'localhost',
                     user = 'root',
                     passwd = '123456',
                     database = 'ele_dict',
                     charset = 'utf8')
cur = db.cursor()
sql = 'insert into words (word,mean) values(%s,%s);'

with open('dict.txt','r') as fd:
    for line in fd:
        re.split(r"\W+")
        cur.execute(sql,[line])
        db.commit()
cur.close()
db.close()