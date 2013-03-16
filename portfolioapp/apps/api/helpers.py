# api/helpers.py

import json
import uuid

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from .models import ApiLog


def log_api_event(request, response, api_key, api_version):
    try:
        l = ApiLog(
            request_id=response['response']['head']['request_id'],
            request_ip_address=request.META['REMOTE_ADDR'],
            request_path=request.path,
            request_method=request.method,
            request_query_string=request.META['QUERY_STRING'],
            request_content_type=request.META['CONTENT_TYPE'],
            request_http_user_agent=request.META['HTTP_USER_AGENT'],
            response_status_code=response['response']['head']['status_code'],
            api_key=api_key,
            api_version=api_version)
        l.save()
    except:
        pass


def api_http_response(request, response):
    version = 'v2'
    apikey = '111222333'
    status_code = 500  # default to error first if we can't retrieve it from the payload

    response['response']['head']['request_id'] = uuid.uuid1().hex

    try:
        status_code = response['response']['head']['status_code']
    except:
        pass

    log_api_event(request, response, apikey, version)
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=status_code)