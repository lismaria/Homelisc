from django.contrib import admin

# Register your models here.
# from django.conf import settings    # alternate for: from Account.models import User
# User = settings.AUTH_USER_MODEL

from Account.models import User
admin.site.register(User)