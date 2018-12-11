import requests
from mymain import myMain

URL = 'https://mc.meitangdehulu.com/message/weblate'
TIMEOUT = 15

@myMain
def main(g,q,m):
    res = requests.get(URL,timeout=TIMEOUT).json()
    if res['status'] =='ok':
        json = res['data'][0]
        return "· 词条翻译进度：%.3f%%\n· 剩余词条：%s\n· 单词翻译进度为：%.3f%% \n· 剩余单词：%s"%(
            json['translated']/json['total'] *100,
            json['total'] - json['translated'],
            json['translated_words']/json['total_words']*100,
            json['total_words'] - json['translated_words'],
        )
    else:
        return '响应超时'