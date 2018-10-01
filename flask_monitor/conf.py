# encoding: utf-8
errors = {
    # 对应exception的type
    'NotResultFoundError':{
        'message': "no result found",
        'status': 404
    },
    'Exception':{
        'message': 'system error, please contact engineer',
        'status': 500
    },
    'OperationalError':{
        'message': 'system error because of mysql',
        'status': 500
    },
    'BadSignature':{
        'message': 'token error because of bad signature',
        'status': 401
    }
}
# TOKEN超时时间为 60 * 60秒
TOKEN_EXPIRES_IN = 60 * 60