from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.is not None
    if response is None:
        response = dict()
        response['responseCode'] = 7
        response['responseDesc'] = 'Service Error'
        return Response(status=200, data=response)

    if response.status_code == 401:
        response.data.pop('detail')
        response.data['responseCode'] = 9060
        response.data['responseDesc'] = 'Unauthorized'
        response.status_code = 200

    elif response.status_code == 400:
        response.data = dict()
        response.data['responseCode'] = 19
        response.data['responseDesc'] = 'data not ok'
        response.status_code = 200

    elif response.status_code == 500:
        response.data = dict()
        response.data['responseCode'] = 7
        response.data['responseDesc'] = 'Service Error'
        response.status_code = 200

    return response
