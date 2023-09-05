from django.contrib import admin

import environ

from ..models import IOLHost

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

admin.site.site_header = "Jembi IOL Admin Platform"
admin.site.index_title = "Welcome to IOL "
admin.site.site_title = "IOL "
admin.site.site_url = "https://cmr-dev.jembi.org/openmrs"

MAX_OBJECTS = 1


class IOLHostAdmin(admin.ModelAdmin):
    list_display = ('host', 'port', 'date_created', 'date_changed',)
    search_fields = ('host',)
    list_per_page = 15

    def has_add_permission(self, request):
        count = IOLHost.objects.all().count()
        if count == 0:
            return True
        return False


admin.site.register(IOLHost, IOLHostAdmin)






















