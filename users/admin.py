from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'is_active', 'is_staff')
    search_fields = ('email', 'phone', 'city')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
