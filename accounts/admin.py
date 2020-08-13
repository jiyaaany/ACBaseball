from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from .forms import UserChangeForm, UserCreationForm
# from .models import Users

# Register your models here.

# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm

#     list_display = ('user_id', 'name', 'email', 'is_admin', 'created_date')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (None, {'fields': ('user_id', 'password')}),
#         ('Personal info', {'fields': ('name', 'email')}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('user_id', 'name', 'email', 'password')}
#          ),
#     )
#     search_fields = ('user_id',)
#     ordering = ('created_date',)
#     filter_horizontal = ()


# admin.site.register(Users, UserAdmin)
# admin.site.unregister(Group)