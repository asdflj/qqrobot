import cqp
import traceback

G = None
Q = None
def myMain(fn):
    def func(g,q,m):
        global G
        global Q
        G = g
        Q = q
        try:
            text = fn(g,q,m)
            if type(text)==str:
                cqp.sendGroupMsg(g,text)
            elif type(text)==int:
                cqp.sendGroupMsg(g,str(text))
            elif text:
                for i in text:
                    cqp.sendGroupMsg(g,i)
        except Exception as e:
            msg(traceback.format_exc())
    return func

def gMsg(text):
    if G:
        cqp.sendGroupMsg(G,text)
    else:
        raise '请装饰main函数'

def pMsg(text):
    if Q:
        cqp.sendPrivateMsg(Q,text)
    else:
        raise '请装饰main函数'

def msg(text):
    gMsg(text)

def qq(text,num=None):
    if num == None:
        gMsg('[CQ:at,qq=%s] %s'%(Q,text))
    else:
        gMsg('[CQ:at,qq=%s] %s'%(num,text))

def atQQ(*args,**kwargs):
    qq(*args,**kwargs)

def sendPic(fileName,text='',method='group'):
    if method =='group':
        gMsg('[CQ:image,file=%s] %s'%(fileName,text))
    elif method == 'private':
        pMsg('[CQ:image,file=%s] %s'%(fileName,text))
    else:
        gMsg('[CQ:image,file=%s] %s'%(fileName,text))

@myMain
def main(g,q,m):
    pass

__all__ = ['myMain','msg','pMsg','gMsg','qq','atQQ','sendPic']