from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Organization(models.Model):
    # org_id = models.IntegerField(null=True)
    # org_id = models.CharField(max_length=7, default='0000000', editable=False)
    org_id = id
    ORG_TYPE_CHOICES = [('customer', 'customer'), ('customer', 'partner')]
    org_type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES, null=True)
    org_name = models.CharField(max_length=50, unique=True)
    domain = models.CharField(max_length=50)

    def __str__(self):
        return self.org_name

class Contact(models.Model):
    phone = models.IntegerField(null=True)
    creation_date = models.DateTimeField("Date Created", null=True)
    ROLE_CHOICES = [('admin', 'admin'), ('user', 'user')]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True)
    STATUS_CHOICES = [('active', 'active'), ('removed', 'removed')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=True)

    def get_contact_org(self):
        return self.organization

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(user=instance)
    instance.contact.save()

class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    product_version = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.product_name

class Entitlement(models.Model):
    # PRODUCT_CHOICES = [("AppLoader", "AppLoader"), ("ScenarioBuilder", "ScenarioBuilder")]
    # product_name = models.CharField(max_length=50, choices=PRODUCT_CHOICES, null=True)
    max_licenses = models.IntegerField(default=100)
    total_licenses = models.IntegerField(default=0)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def get_product_name(self):
        return self.product.product_name

    def get_version_number(self):
        return self.product.product_version

    def get_organization_name(self):
        return self.organization.org_name

    def get_entitlement_dictionary(self):
        entitlement_dict = {}
        num_allocated = str(self.total_licenses) + " of " + str(self.max_licenses)
        entitlement_dict["product_name"] = self.product.product_name
        entitlement_dict["access_code"] = self.product.product_version
        entitlement_dict["num_allocated"] = num_allocated
        return entitlement_dict

    def check_allocated_licenses(self):
        remaining_licenses = self.max_licenses - self.total_licenses
        if remaining_licenses < self.max_licenses:
            return True

        else:
            return False

    def get_entitlement_name(self):
        return self.organization.org_name + "/" + self.product.product_name

    def __str__(self):
        return self.organization.org_name + "/" + self.product.product_name
