import typing

from django.http import HttpRequest
from rest_framework_api_key.permissions import HasAPIKey

from empo_news.APIKeyManager import APIKeyManager
from empo_news.errors import UnauthenticatedException
from empo_news.models import UserFields


class KeyPermission(HasAPIKey):
    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        key = request.META.get('HTTP_API_KEY', '')

        if not key:
            raise UnauthenticatedException

        api_key = APIKeyManager.get_hash_key(key)

        try:
            UserFields.objects.get(api_key=api_key)
        except UserFields.DoesNotExist:
            raise UnauthenticatedException

        return True
