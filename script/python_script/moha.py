from mymain import *
i = 0
@myMain
def main(g,q,m):
    global i
    if i == -1:
        return 'hello, world'
    i += 1
    main(g,q,m)