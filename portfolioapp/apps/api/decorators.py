# api/decorators.py

from functools import wraps

from .helpers import verify_token, api_http_response, HttpMessages


def token_required(fn):
    @wraps(fn)
    def _wrapped_view(request, *args, **kwargs):
        token = request.REQUEST.get('token')
        identifier = request.REQUEST.get('identifier')

        if identifier and token:
            user = verify_token(token, identifier)
            if user:
                return fn(request, user, *args, **kwargs)

        response = {
            'response': {
                'meta': {
                    'status_code': 401,
                    'message': HttpMessages.UNAUTHORIZED
                }
            }
        }

        return api_http_response(request, response)
    return _wrapped_view