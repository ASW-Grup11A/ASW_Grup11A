from rest_framework.exceptions import APIException


class UrlAndTextFieldException(APIException):
    status_code = 400
    default_detail = 'Submissions can\'t have both urls and text, so you need to pick one. If you keep the url, ' \
                     'you can always post your text as a comment in the thread.'
    default_code = 'url and text filled'


class TitleIsTooLongException(APIException):
    status_code = 400
    default_detail = 'Title is too long (maximum is 80 characters)'
    default_code = 'title too long'


class UrlIsTooLongException(APIException):
    status_code = 400
    default_detail = 'Url is too long (maximum is 500 characters)'
    default_code = 'url too long'


class UnauthenticatedException(APIException):
    status_code = 401
    default_detail = 'The user is not authenticated'
    default_code = 'not authenticated'
