from logging import Logger
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.translation import gettext
from django.conf import settings
from voluptuous import MultipleInvalid
from st1_voluptuous_serializable import voluptuous_dict


logger = Logger(__name__)


def handle_voluptuous_invalid(error: MultipleInvalid, request: HttpRequest):
    return JsonResponse(voluptuous_dict(error), status=400)


class St1ExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) \
        -> HttpResponse | None:
        if isinstance(exception, MultipleInvalid):
            return handle_voluptuous_invalid(exception, request)

        logger.exception('unhandled exception')

        if settings.DEBUG:
            return None

        return JsonResponse({
            'error': gettext('Unexpected Error Occurred')
        }, status=500)

