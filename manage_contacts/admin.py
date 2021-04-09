from django.contrib import admin
from .models import Organization, Contact, Product

#Show org ID as readonly field
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Contact)
admin.site.register(Product)
# admin.site.register(Entitlement)
