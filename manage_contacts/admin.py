from django.contrib import admin
from .models import Contact, Organization, Entitlement

# Register your models here.
admin.site.register(Organization)
admin.site.register(Entitlement)
admin.site.register(Contact)
