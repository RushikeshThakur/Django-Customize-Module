from django.contrib import admin
# from .models import Profile
# Register your models here.
# admin.site.register(Profile)
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import MyUser, Profile, ActivationProfile


class UserAdmin(BaseUserAdmin): #control display via admin page 
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email','is_admin','is_staff','is_active')  # admin display field main
    list_filter = ('is_admin','is_staff','username') #filter display at admin page
    fieldsets = (   # edit time
        (None, {'fields': ('username','email', 'password')}),
        #('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')}),
        ('Access', {'fields': ('is_active',)}),
    )   
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = ( # add time
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2','is_staff','is_admin'),
        }),
    )
    search_fields = ('username','email',)  # searching via email id and password
    ordering = ('username','email',)  # sorting
    filter_horizontal = ()
    


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(Profile)
admin.site.register(ActivationProfile)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)