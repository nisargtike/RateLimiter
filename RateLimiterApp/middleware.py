from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from RateLimiterApp.rate_limiter import SlidingWindowCounterRateLimiter
from django.http import HttpResponseForbidden

class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda:self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JSONWebTokenAuthentication()
        if jwt_authentication.get_jwt_value(request):
            user, jwt = jwt_authentication.authenticate(request)
        return user


class RateLimiterMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = str(SimpleLazyObject(lambda:JWTAuthenticationMiddleware.get_jwt_user(request)))
        if(username=="AnonymousUser"):
            return self.get_response(request)
        ip = request.META['REMOTE_ADDR']
        s = SlidingWindowCounterRateLimiter()
        if s.shouldAllowServiceCall(username, ip)==False:
            return HttpResponseForbidden()
        return self.get_response(request)