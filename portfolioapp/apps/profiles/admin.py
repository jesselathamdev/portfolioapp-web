# profiles/admin.py
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User
from .forms import CreateUserProfileForm

class UserChangeForm(forms.ModelForm):
    """ A form for updating users. Includes all the fields
        on the user, but replaces the password field with
        admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the
        # initial value. This is done here, rather than on
        # the field, because the field does not have access
        # to the initial value
        return self.initial["password"]


class UserAdmin(UserAdmin):
    # Set the add/modify forms
    add_form = CreateUserProfileForm
    form = UserChangeForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff', 'first_name', 'last_name',)
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'groups',)
    search_fields = ('email', 'first_name', 'last_name',)
    readonly_fields = ('last_login', 'date_created', 'date_updated',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        ('Personal info', {'fields': ('email', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': (('last_login', 'date_created', 'date_updated'),)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2',)}
        ),
    )

# Register the new UserAdmin
admin.site.register(User, UserAdmin)