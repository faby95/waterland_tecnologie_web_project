from django.contrib import admin
from userpark.models import User as myUser
from userpark.models import StaffAuthTable
from django.contrib.auth.models import Group


@admin.action(description='Invalid selected keys')
def make_invalid_keys(modeladmin, request, queryset):
    queryset.update(is_used=True)

# Register your models here.
# admin.site.register


@admin.register(myUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff_member', 'date_joined', 'staff_assigned_code')
    exclude = ('staff_assigned_code', 'propic', 'password', 'groups', 'user_permissions', 'is_active')
    list_filter = (
        ('is_staff_member', admin.BooleanFieldListFilter),
        ('date_joined', admin.DateFieldListFilter),
    )


@admin.register(StaffAuthTable)
class StaffAuthTableAdmin(admin.ModelAdmin):
    list_display = ('code', 'key', 'is_used')
    list_filter = (
        ('is_used', admin.BooleanFieldListFilter),
    )
    actions = [make_invalid_keys]


admin.site.unregister(Group)
