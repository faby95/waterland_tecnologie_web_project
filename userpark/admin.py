from django.contrib import admin
from userpark.models import User as myUser
from userpark.models import StaffAuthTable
from django.contrib.auth.models import Group

# Register your models here.


@admin.register(myUser)
class UserAdmin(admin.ModelAdmin):
    exclude = ('staff_assigned_code', 'propic', 'password', 'groups', 'user_permissions', 'is_active')
    list_filter = (
        ('is_staff_member', admin.BooleanFieldListFilter),
        ('date_joined', admin.DateFieldListFilter),
    )


@admin.register(StaffAuthTable)
class StaffAuthTableAdmin(admin.ModelAdmin):
    list_filter = (
        ('is_used', admin.BooleanFieldListFilter),
    )


admin.site.unregister(Group)
