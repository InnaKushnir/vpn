from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'date_joined')
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)
