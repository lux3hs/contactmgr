from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    # org_id = models.IntegerField(null=True)
    # org_id = models.CharField(max_length=7, default='0000000', editable=False)
    org_id = id
    ORG_TYPE_CHOICES = [('CUSTOMER', 'customer'), ('PARTNER', 'partner')]
    org_type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES, null=True)
    org_name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)

    def __str__(self):
        return self.org_name

class Entitlement(models.Model):
    product_name = models.CharField(max_length=50)
    max_licenses = models.IntegerField(default=100)
    total_licenses = models.IntegerField(default=0)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    phone = models.IntegerField(null=True)
    creation_date = models.DateTimeField("Date Created")
    ROLE_CHOICES = [('admin', 'admin'), ('user', 'user')]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True)
    STATUS_CHOICES = [('active', 'active'), ('removed', 'removed')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username
