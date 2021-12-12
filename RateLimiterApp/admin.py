from django.contrib import admin
from django.contrib.auth.models import Group, User
from RateLimiterApp.models import *

# admin.site.unregister(Group)
# admin.site.unregister(User)

admin.site.register(CustomUser)