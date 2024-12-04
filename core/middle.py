import json
from django.shortcuts import HttpResponse
from django.core.handlers.exception import response_for_exception


class ExceptionChatbot:
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        self.response = self.get_response(request)
        return self.response

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        exception_handle_message = response_for_exception(request, exception)
        if exception_handle_message.status_code == 500:
            response_data = dict()
            response_data['responseCode'] = 7
            response_data['responseDesc'] = 'Service Error'
            res = HttpResponse(json.dumps(response_data), content_type="application/json")
            res.status_code = 200
            return res
        else:
            return None
