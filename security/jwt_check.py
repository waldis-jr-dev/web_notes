import jwt
import os
import time


def jwt_ttl_check(encoded_jwt_token: str) -> bool:
    if encoded_jwt_token['ttl'] > int(time.time()):
        return True
    else:
        False


def jwt_check(function):
    def wrapper(*args, **kwargs):
        token = request.cookies['session_token']
        if not token:
            redirect('/login')
        try:
            jwt.decode(token, os.getenv('JWT_KEY'))
        except jwt.ExpiredSignature:
            redirect('/login')
        return function(*args, **kwargs)
    return wrapper()
