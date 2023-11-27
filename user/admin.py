from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.urls import path

from common.admin import admin_site
from .models import User, NewSignup, Profile, Memo
from .signals import signup_denied, signup_approved


class ProfileInline(admin.StackedInline):
    model = Profile
    autocomplete_fields = ('water_utility', )

class ProfileReadonlyInline(ProfileInline):
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(User, site=admin_site)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    inlines = (ProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        obj.username = obj.email
        obj.save()


@admin.register(NewSignup, site=admin_site)
class NewSignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    fields = ('first_name', 'last_name', 'email', 'role', 'date_joined')
    inlines = (ProfileReadonlyInline,)

    def save_model(self, request, obj, form, change):
        obj.profile.is_approved = True
        obj.profile.save()
        signup_approved.send(sender=self.__class__, user=obj)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        signup_denied.send(sender=self.__class__, user=obj)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(profile__is_approved=False)


@admin.register(Profile, site=admin_site)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'water_utility', 'phone_number', 'subscribe_desc',)
    search_fields = ('user',)
    list_filter = ('is_approved',)
    autocomplete_fields = ('user', 'water_utility', )


@admin.register(Memo, site=admin_site)
class MemoAdmin(admin.ModelAdmin):
    list_display = ('memo', 'email_domain')
    search_fields = ('memo', 'email_domain')
