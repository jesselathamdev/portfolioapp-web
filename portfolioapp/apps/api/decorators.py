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


def paginate(fn):
    @wraps(fn)
    def _wrapped_view(request, *args, **kwargs):
        OFFSET = 0
        LIMIT = 3
        try:
            LIMIT = int(request.GET.get('limit', LIMIT))
            OFFSET = int(request.GET.get('offset', OFFSET))
        except:
            pass

        return fn(request, *args, limit=LIMIT, offset=OFFSET, **kwargs)
    return _wrapped_view