COOLQ_ROBOT_SECRET = None
COOLQ_ROBOT_ACCESS_TOKEN = None
CORE_MIDDLEWARE = [
    'handler.my_middleware.HMAC_Signature',
    'handler.my_middleware.RequestMethod',
    'handler.my_middleware.Transjson',
    'handler.my_middleware.Escape',
]
EVENT_MIDDLEWARE = {
    'message':[
        'handler.event.middleware.SavePic',
        'handler.event.middleware.Ping',
        'handler.event.middleware.Import_py', #core middleware
        'handler.event.middleware.Bind',
        'handler.event.middleware.Disable',
        'handler.event.middleware.Enable',
        'handler.event.middleware.List',
        'handler.event.middleware.Print',
        'handler.event.middleware.RunScript',
        'handler.event.middleware.Eval',
        'handler.event.middleware.Help',
    ],
    'notice':[

    ],
    'request':[

    ],
    'meta_event':[
        
    ]
}

ADMIN = [854865755]
BLACK_LIST = ['cqp','__init__','os','sys']
SERVER = 'http://192.168.1.115:5700'