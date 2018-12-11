import cqp
from mymain import *
import numpy as np

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
    return '你掷出了%s枚硬币\n正面:%s次\n背面:%s次'%(
        num,result['front'],result['back']
    )

def coin(num):
    total = {'front': 0, 'back': 0}
    result=np.random.binomial(1,0.5,num).tolist()
    total['front'] = result.count(0)
    total['back'] = result.count(1)
    return total