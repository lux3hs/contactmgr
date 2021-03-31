from django.db import models

# Create your models here.
class License(models.Model):
    """ License database model """
    organization = models.CharField(max_length=50, null=True)
    product = models.CharField(max_length=50, null=True)
    max_licenses = models.CharField(max_length=50, null=True)
    total_licenses = models.CharField(max_length=50, null=True)
    creator_email = models.CharField(max_length=50, null=True)
    creator_phone = models.CharField(max_length=50, null=True)
    re_seller = models.CharField(max_length=50, null=True)
    host_ip = models.CharField(max_length=50, null=True)
    is_permanent = models.CharField(max_length=50, null=True)
    product_grade = models.CharField(max_length=50, null=True)
    product_stations = models.CharField(max_length=50, null=True)
    allowed_ips = models.CharField(max_length=50, null=True)
    creation_date = models.CharField(max_length=50, null=True)
    expiration_date = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.organization) + "-" + str(self.product) + str(self.creation_date)