import json
import os
import sys
from werkzeug.exceptions import HTTPException
from flask import Flask, request, _request_ctx_stack, abort, session, redirect, jsonify
from functools import wraps
from dotenv import load_dotenv, find_dotenv
from jose import jwt
from urllib.request import urlopen
from os import environ

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://0.0.0.1:8080'

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    # print("get token auth header start")
    try:
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # print(auth_header)
            if auth_header:
                bearer_token_array = auth_header.split(' ')
                if bearer_token_array[0] and bearer_token_array[0].lower() == "bearer" and bearer_token_array[1]:
                    token = bearer_token_array[1]
                    # print("auth token: " + token)
    except Exception:
        raise AuthError({
            'error': 'Authorization header is expected.',
            'status_code': 401
        }, 401)
    return token


'''
check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string
    is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        # print("missing permissions")
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        # print("permission not found")
        raise AuthError({
            'code': 'unauthorized',
            'status_code': 'Permission not found.'
        }, 401)
    return True


'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/
    scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # print(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        # print("missing kid")
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        # print('rsa_key exists')
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            # print("expired signature error")
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            # print("jwt claims error")
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. ' +
                               'Please, check the audience and issuer.'
            }, 401)

        except Exception:
            # print("exception invalid header error")
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims
        and check the requested permission
    return the decorator which passes
        the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = session['token']
            except:
                try:
                    token = get_token_auth_header()
                except:
                    print("token is none")
                    abort(401)
            # print('token at authorization time: {}'.format(token))
            try:
                payload = verify_decode_jwt(token)
                # print('Payload is: {}'.format(payload))
                # print(f'testing for permission: {permission}')
            except Exception:
                # print("verify decode jwt error")
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
