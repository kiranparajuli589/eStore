from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, Customer, UserProfile


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


class MyCustomerAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'address', 'phone', 'email', 'tot_due', 'tot_received')
    search_fields = ('f_name', 'l_name', 'email', 'address', 'phone', 'date_created')
    list_filter = ('address', 'date_created')
    date_hierarchy = 'date_created'
    ordering = ('-date_created',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone' )
    search_fields = ('address', 'phone')
#    list_filter = ('address', 'date_created')
#    date_hierarchy = 'date_created'
#    ordering = ('-date_created',)


admin.site.register(User, MyUserAdmin)
admin.site.register(Customer, MyCustomerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(Group)