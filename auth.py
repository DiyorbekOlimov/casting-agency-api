import os
import json
from functools import wraps
from urllib.request import urlopen
from flask import request
from jose import jwt

AUTH0_DOMAIN = 'diyorbek.us.auth0.com'
API_AUDIENCE = 'casting'
ALGORITMS = ['RS256']


class AuthError(Exception):
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError(401, 'authorization header excepted')
    
    parts = auth.split()
    if parts[0].lower() != 'bearer': raise AuthError(401, 'bearer token not found')
    
    if len(parts) != 2: raise AuthError(401, 'authorization header must be bearer token')
    
    return parts[1]

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_token = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_token: raise AuthError(401, 'authorization malformed')

    for key in jwks['keys']:
        if key['kid'] == unverified_token['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError(401, 'jwt token expired')
        except jwt.JWTClaimsError:
            raise AuthError(401, 'invalid claims')
        
        except Exception: raise AuthError(400, 'unable to parse authorization token')

def check_permissions(permission, payload):
    if 'permissions' not in payload: raise AuthError(400, 'permission not included in jwt')
    if permission not in payload['permissions']: raise AuthError(401, 'permission not found')
    return True

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except: raise AuthError(401, 'jwt not verified')
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
