COOLQ_ROBOT_SECRET = None
COOLQ_ROBOT_ACCESS_TOKEN = None

MESSAGE_TYPE = {
    'MESSAGE':'message',
    'NOTICE':'notice',
    'REQUEST':'request',
    'META_EVENT':'meta_event',
}

CORE_MIDDLEWARE = [
    'handler.my_middleware.HMAC_Signature',
    'handler.my_middleware.RequestMethod',
    'handler.my_middleware.Transjson',
    'handler.my_middleware.Escape',
]
EVENT_MIDDLEWARE = {
    MESSAGE_TYPE['MESSAGE']:[
        'handler.event.middleware.Debug',
        'handler.event.middleware.Ping',
        'handler.event.middleware.Version',
        'handler.event.middleware.SavePic',
        'handler.event.middleware.Import_py',
        'handler.event.middleware.Bind',
        'handler.event.middleware.Disable',
        'handler.event.middleware.Enable',
        'handler.event.middleware.List',
        'handler.event.middleware.Print',
        'handler.event.middleware.Eval',
        'handler.event.middleware.Help',
        'handler.event.middleware.Register',#注册第三方中间件
        'handler.event.middleware.UnRegister',
        'handler.event.middleware.RunThirdPartyMiddleware',
        'handler.event.middleware.RunScript',
    ],
    MESSAGE_TYPE['NOTICE']:[
        'handler.event.middleware.RunThirdPartyMiddleware',
    ],
    MESSAGE_TYPE['REQUEST']:[
        'handler.event.middleware.RunThirdPartyMiddleware',
    ],
    MESSAGE_TYPE['META_EVENT']:[
        'handler.event.middleware.RunThirdPartyMiddleware',
    ]
}

ADMIN = [854865755]
BLACK_LIST = ['cqp','__init__','os','sys']
SERVER = 'http://192.168.1.103:5700'
DEBUG = {'mode':False,'user_id':854865755}
VERSION = ('alpha',0.2)