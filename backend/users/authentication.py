from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.request import Request


class CookieJWTAuthentication(JWTAuthentication):
    """
    Reads the access_token from the HttpOnly cookie
    instead of the Authorization header.
    """

    def authenticate(self, request: Request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None  # no token found — let DRF handle as unauthenticated

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except:
            return None
