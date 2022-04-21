from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


# def group(self, user):
#     groups = []
#     for group in user.groups.all():
#         groups.append(group.name)
#     return ' '.join(groups)


# group.short_description = 'Groups'
#
# list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'group')


class UserAdminWithGroup(UserAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'group')


class GroupAdminWithCount(GroupAdmin):
    def user_count(self, obj):
        return obj.user_set.count()

    list_display = GroupAdmin.list_display + ('user_count',)


admin.site.register(Profile)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdminWithCount)
admin.site.unregister(User)
admin.site.register(User, UserAdminWithGroup)
