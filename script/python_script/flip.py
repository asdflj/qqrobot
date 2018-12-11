import random
from mymain import *

@myMain
def main(g,q,m):
    if len(m):
        return random.choice(m.split(' '))
    else:
        return '参数错误'