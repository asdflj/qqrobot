COOLQ_ROBOT_SECRET = '123456'
COOLQ_ROBOT_ACCESS_TOKEN = '1'
CORE_MIDDLEWARE = [
    'handler.my_middleware.RequestMethod',
    'handler.my_middleware.Transjson',
    # 'handler.my_middleware.HMAC_Signature',
    # 'handler.my_middleware.Access_token'
]
EVENT_MIDDLEWARE = {
    'message':[
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
BLACK_LIST = ['cqp']
SERVER = 'http://192.168.1.114:5700'