from django.contrib import admin
from .models import Contact, Organization, Entitlement

#Show org ID as readonly field
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Entitlement)
admin.site.register(Contact)
