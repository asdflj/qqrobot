import cqp
import random
from mymain import *

@myMain
def main(g,q,m):
    if not len(m):
        num = 10
    elif m.isdigit():
        num = int(m)
        if 1 > num or num > 999:
            return '范围在1-999之间'
    else:
        return '输入错误次数必须为整数数字'

    result =coin(num)
    return '你掷出了%s枚硬币\n正面:%s次\n背面:%s次\n立起来:%s次'%(
        num,result['front'],result['back'],result['stand']
    )

def coin(num):
    stand = int(random.random() * 100)
    total = {'front': 0, 'back': 0, 'stand': 0}

    for i in range(num):
        result = int(random.random() * 100)
        if stand == result:
            total['stand'] += 1
        elif 0 < result < 50:
            total['back'] += 1
        else:
            total['front'] += 1
    return total