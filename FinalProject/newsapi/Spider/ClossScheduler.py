# -*- coding：utf-8 -*-
import os


def kill(pid):
    # 本函数用于中止传入pid所对应的进程
    if os.name == 'nt':
        # Windows系统
        cmd = 'taskkill /pid ' + str(pid) + ' /f'
        try:
            os.system('chcp 65001')
            os.system(cmd)

            print(pid, 'killed')
        except Exception as e:
            print(e)
    elif os.name == 'posix':
        # Linux系统
        cmd = 'kill ' + str(pid)
        try:
            os.system(cmd)
            print(pid, 'killed')
        except Exception as e:
            print(e)
    else:
        print('Undefined os.name')


def getpidandkill(filename):
    f1 = open(file=filename + '.txt', mode='r')

    pid = f1.read()
    f1.close()

    # 调用kill函数，终止进程
    kill(pid=pid)
