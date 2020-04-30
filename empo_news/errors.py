from rest_framework.exceptions import APIException


class UrlAndTextFieldException(APIException):
    status_code = 400
    default_detail = 'Submissions can\'t have both urls and text, so you need to pick one. If you keep the url, ' \
                     'you can always post your text as a comment in the thread.'
    default_code = 'url and text filled'
