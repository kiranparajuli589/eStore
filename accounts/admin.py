from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, Customer, UserProfile, Vendor, ResetPasswordCode


class MyUserAdmin(UserAdmin):
    list_display = ("upper_case_name", "email", "address", "phone", "date_created", "is_admin", "is_staff", "is_active")
    list_filter = ("address", "is_admin", "is_staff", "is_active",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("f_name", "l_name", "address", "phone")}),
        ("Permissions", {"fields": ("is_admin", "is_staff", "is_active")})
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "f_name", "l_name", "password1", "password2")}
         ),
    )

    search_fields = ("email", "f_name")
    date_hierarchy = "date_created"
    ordering = ("f_name", "date_created")

    filter_horizontal = ()


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("get_customer_name", "address", "phone", "email", "tot_due", "tot_received")
    search_fields = ("f_name", "l_name", "email", "address", "phone")
    list_filter = ("address", "date_created")
    date_hierarchy = "date_created"
    ordering = ("-date_created",)


class VendorAdmin(admin.ModelAdmin):
    list_display = ("get_vendor_name", "address", "phone", "email", "tot_due", "tot_received")
    search_fields = ("f_name", "l_name", "email", "address", "phone")
    list_filter = ("address", "date_created")
    date_hierarchy = "date_created"
    ordering = ("-date_created",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio", "get_user_address", "get_user_phone")
    search_fields = ("user__f_name", "user__l_name", "user__address", "user__phone")
    list_filter = ("user__address", "user__date_created")
    date_hierarchy = "user__date_created"


admin.site.register(User, MyUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ResetPasswordCode)
admin.site.unregister(Group)
