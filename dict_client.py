"""
dict 客户端
"""

from socket import *
from getpass import getpass

ADDR = ('127.0.0.1', 8009)
# 所有函数都需要s
s = socket()
s.connect(ADDR)


# 注册
def do_register():
    while True:
        name = input("User:")
        passwd = getpass("passwd:")
        passwd1 = getpass("Again:")

        if (' ' in name) or (' ' in passwd):
            print("用户名或密码不能有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue

        msg = "R %s %s" % (name, passwd)
        # 发送请求
        s.send(msg.encode())
        # 接收反馈
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


# 登录
def do_login():
    name = input("User:")
    passwd = getpass("passwd:")
    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())
    # 等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")


# 查单词
def do_query(name):
    while True:
        word = input("请输入你想要查询的单词(##退出):")
        if word == '##':  # 结束查询
            break
        msg = "Q %s %s" % (name, word)
        s.send(msg.encode())  # 发送给服务端
        # 等待反馈
        data = s.recv(2048).decode()
        print(data)
        # if data == 'False':
        #     print("查询失败")
        # else:
        #     print("%s mean: %s"%(word,data))


# 查找历史记录
def do_hist(name):
    msg = "H %s" % name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)

    else:
        print("没有历史记录")


# 二级界面
def login(name):
    while True:
        print("""
        =============Query==============
        1.查单词     2.历史记录      3.注销
        ================================
        """)
        cmd = input("请输入选项：")  # cmd:命令
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_hist(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确命令！")


# 创建网络连接
def main():
    while True:
        print("""
        ============Welcome=============
        1.注册        2.登录        3.退出
        ================================
        """)
        cmd = input("请输入选项：")  # cmd:命令
        if cmd == '1':
            # s.send(cmd.encode())    #测试代码
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            print("谢谢使用")
            return
        else:
            print("请输入正确命令！")


if __name__ == '__main__':
    main()
