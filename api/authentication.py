import datetime
from django.utils.timezone import utc
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
import pytz 

class ExpiringTokenAuthentication(TokenAuthentication):
    """
    source: https://stackoverflow.com/questions/14567586/token-authentication-for-restful-api-should-the-token-be-periodically-changed
    """
    def authenticate_credentials(self, key):

        try:
            self.model = self.get_model() 
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) 

        if token.created < utc_now - datetime.timedelta(hours=1):
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)