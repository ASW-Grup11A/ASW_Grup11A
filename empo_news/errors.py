from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def empo_news_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status'] = response.status_code
        response.data['error'] = exc.get_codes()
        response.data['message'] = exc.detail
        del response.data['detail']

    return response


class UrlAndTextFieldException(APIException):
    status_code = 400
    default_detail = 'Submissions can\'t have both urls and text, so you need to pick one. If you keep the url, ' \
                     'you can always post your text as a comment in the thread.'
    default_code = 'Bad Request'


class TitleIsTooLongException(APIException):
    status_code = 400
    default_detail = 'Title is too long (maximum is 80 characters)'
    default_code = 'Bad Request'


class UrlIsTooLongException(APIException):
    status_code = 400
    default_detail = 'Url is too long (maximum is 500 characters)'
    default_code = 'Bad Request'


class InvalidQueryParametersException(APIException):
    status_code = 400
    default_detail = 'Url and ask parameters cannot be used together'
    default_code = 'Bad Request'


class UrlCannotBeModifiedException(APIException):
    status_code = 400
    default_detail = 'Url contributions cannot be modified'
    default_code = 'Bad Request'


class UnauthenticatedException(APIException):
    status_code = 401
    default_detail = 'The user is not authenticated'
    default_code = 'Unauthorized'


class ForbiddenException(APIException):
    status_code = 403
    default_detail = 'Your api key (Api-Key Header) is not valid'
    default_code = 'Forbidden'


class NotFoundException(APIException):
    status_code = 404
    default_detail = 'No item with that ID'
    default_code = 'Not Found'


class ConflictException(APIException):
    status_code = 409
    default_detail = 'The contribution already is in this state'
    default_code = 'Conflict'


class ContributionUserException(APIException):
    status_code = 409
    default_detail = 'The contribution is yours'
    default_code = 'Conflict'
