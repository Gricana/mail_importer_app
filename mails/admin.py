from django.contrib import admin

from .models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ('account', 'subject', 'date_sent', 'body', )
    search_fields = ('account__email', 'subject', 'date_sent', )


admin.site.register(Email, EmailAdmin)
