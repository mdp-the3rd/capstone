import json
from functools import wraps
from flask import request, abort
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
ALGORITHMS = os.environ.get('RS256')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        abort(401)

    parts = auth.split()
    if parts[0].lower() != "bearer":
        abort(401)
    elif len(parts) == 1:
        abort(401)
    elif len(parts) > 2:
        abort(401)

    return parts[1]

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(403)

    if permission not in payload['permissions']:
        abort(403)

    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_key:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload

    abort(401)

def requires_auth(permission=''):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return decorator
