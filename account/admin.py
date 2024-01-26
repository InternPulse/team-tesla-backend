'''
Customize django admin for account app
'''

from django.contrib import admin

from .models import CustomUser, Token


class CustomUserAdmin(admin.ModelAdmin):
    '''CustomUser model customization'''
    ordering = ['id']
    list_display = ['id', 'first_name', 'last_name', 'email', 'email_verified', 'accepted_terms', 'business', 'is_staff', 'is_active', 'created_at', 'updated_at']
    readonly_fields = ['last_login', 'password']

    fieldsets = (
        (None,{'fields':('first_name', 'last_name', 'email', 'password', 'last_login')}),
        ('permissions',{'fields':('email_verified', 'accepted_terms', 'business', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')})      
    )

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('first_name', 'last_name', 'email', 'password1', 'password2', 'email_verified', 'accepted_terms', 'business', 'is_staff',
            'is_superuser', 'is_active', 'groups', 'user_permissions'
            )}
        ),
    )

    search_fields = ['id', 'email', 'first_name', 'last_name']

    list_editable = ['email_verified', 'accepted_terms', 'business', 'is_staff', 'is_active']

    list_filter = ['email_verified', 'accepted_terms', 'business', 'is_staff', 'is_active', 'is_superuser']


class TokenAdmin(admin.ModelAdmin):
    '''Token model customization'''
    ordering = ['id']
    list_display = ['id', 'user_id', 'access', 'refresh']

    search_fields = ['id', 'user_id', 'access', 'refresh']


# Register models with their respective class.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Token, TokenAdmin)
