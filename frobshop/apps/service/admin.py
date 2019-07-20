from django.contrib import admin
from .models import service,category,ServiceImage

# Register your models here.
class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 3


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ ServiceImageInline, ]


admin.site.register(service, ServiceAdmin)
admin.site.register(category)

