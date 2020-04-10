from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


class MyUserAdmin(UserAdmin):
    list_display = ('upper_case_name', 'email', 'date_created', 'is_admin', 'is_staff', 'is_active')
    list_filter = ('is_admin', 'email')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('f_name', 'l_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'f_name', 'l_name', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'f_name')
    date_hierarchy = 'date_created'
    ordering = ('f_name', 'date_created')

    filter_horizontal = ()

# just for reference
# class LogAdmin(admin.ModelAdmin):
#     list_display = ('date', 'user', 'subject', 'detail')
#     search_fields = ('user', 'date')
#     list_filter = ('user', 'date', 'subject')
#     date_hierarchy = 'date'
#     ordering = ('-date', 'user')


admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
