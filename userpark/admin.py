from django.contrib import admin

from userpark.models import User as myUser
from django.contrib.auth.models import Group

# Register your models here.


admin.site.register(myUser)
admin.site.unregister(Group)
