# api/helpers.py

import json
import uuid

from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import ApiLog, ApiToken


class HttpMessages(object):
    OK = 'OK'  # 200
    CREATED = 'Created'  # 201
    UNAUTHORIZED = 'Unauthorized'  # 401
    FORBIDDEN = 'Forbidden'  # 403
    NOT_FOUND = 'Not Found'  # 404
    METHOD_NOT_ALLOWED = 'Method Not Allowed'  # 405
    INTERNAL_SERVER_ERROR = 'Internal Server Error'  # 500
    NOT_IMPLEMENTED = 'Not Implemented'  # 501


def log_api_event(request, response, api_key, api_version):
    # watch out as this might blow up when it changes to a POST

    # mask the password field so that it doesn't end up in the logs
    q = request.GET.copy()
    if 'password' in q:
        q.__setitem__('password', '********')

    query_string = "&".join(["%s=%s" % (k, v) for k, v in q.items()])

    try:
        l = ApiLog(
            request_id=response['response']['meta']['request_id'],
            request_ip_address=request.META['REMOTE_ADDR'],
            request_path=request.path,
            request_method=request.method,
            request_query_string=query_string,
            request_http_user_agent=request.META['HTTP_USER_AGENT'],
            response_status_code=response['response']['meta']['status_code'],
            api_key=api_key,
            api_version=api_version)
        l.save()
    except Exception, e:
        print("There was an error with the api logging module: %s" % e.message)
        pass


def api_http_response(request, response):
    version = 'v2'
    apikey = '111222333'

    response['response']['meta']['request_id'] = uuid.uuid1().hex

    status_code = response['response']['meta']['status_code']

    log_api_event(request, response, apikey, version)
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=status_code)


def create_token(user, identifier):
    try:
        token = uuid.uuid1().hex
        ApiToken.objects.all().filter(user=user, identifier=identifier).delete()  # remove any tokens that have the same identifier for the user
        t = ApiToken(user=user, token=token, identifier=identifier, date_expires=None)
        t.save()
    except Exception, e:
        token = None
        pass

    return token


def verify_token(token, identifier):
    try:
        user = ApiToken.objects.select_related().get(token=token, identifier=identifier).user
        if user.is_active:
            return user
    except ObjectDoesNotExist, e:
        pass

