"""
    dict 服务端
    处理请求逻辑
"""

from socket import *
from multiprocessing import Process
import signal
import sys
from time import sleep
from operation_db import *

# 全局变量
HOST = '0.0.0.0'
PORT = 8009
ADDR = (HOST, PORT)  # 服务端地址


# 网络搭建
def main():
    # 先创建数据库连接对象
    db = Database()  # 模块operation_db

    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    print("Listen the port 8000")
    while True:
        try:
            c, addr = s.accept()
            print("Connect from ", addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 没出现异常，说明正常连接，创建子进程,由子进程去处理客户端请求
        p = Process(target=do_request, args=(c, db))
        p.daemon = True
        p.start()


# 处理客户端请求
def do_request(c, db):
    db.create_cursor()  # 生成游标   du.cur
    while True:
        data = c.recv(1024).decode()
        # print(data)
        # 开始写客户端
        print(c.getpeername(), ':', data)
        if not data or data[0] == 'E':  # 退出
            db.close()
            c.close()
            sys.exit("客户端退出")
        elif data[0] == 'R':  # 注册
            do_register(c, db, data)
        elif data[0] == 'L':  # 登录
            do_login(c, db, data)
        elif data[0] == 'Q':  # 查询单词
            do_query(c, db, data)
        elif data[0] == 'H':  # 历史记录
            do_hist(c, db, data)

#历史记录
def do_hist(c, db, data):
    name = data.split(' ')[1]

    r = db.history(name)

    if not r:
        # 没有历史记录
        c.send(b'FAIL')
        return
    c.send(b'OK')
    for i in r:
        # i --->(name,word,time)
        msg = "%s   %s   %s" % i
        sleep(0.1)  # 防止粘包
        c.send(msg.encode())

    sleep(0.1)
    c.send(b'##')


# 处理查找
def do_query(c, db, data):
    tmp = data.split(' ')  # Q，name,word
    name = tmp[1]
    word = tmp[2]

    # 插入历史记录
    db.insert_history(name, word)

    # 查单词，没查到 返回None
    means = db.query(word)
    if means:
        msg = "%s : %s" % (word, means)
        c.send(msg.encode())
        # c.send(means[0].encode())
    else:
        c.send(b'False')


# 处理登录
def do_login(c, db, data):
    tmp = data.split(' ')  # 按空格切片  得到三部分，头，name,passwd
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')


# 处理注册
def do_register(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]

    # 数据库操作数据
    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')


if __name__ == '__main__':
    main()
