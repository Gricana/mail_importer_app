from django.contrib import admin

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', )
    search_fields = ('email', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
    )
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)
admin.site.site_header = 'Импорт почты'
