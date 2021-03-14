from django.db import models

# Create your models here.
class License(models.Model):
    """ License database model """
    org_name = models.CharField(max_length=50, null=True)
    org_id = models.IntegerField(default=0, null=True)
    entitlement_id = models.IntegerField(default=0, null=True)
    IP_Host = models.CharField(max_length=50, null=True)
    creator_email = models.CharField("Created by ", max_length=50, null=True)
    creator_phone = models.IntegerField(default=0, null=True)
    
    product_name = models.CharField(max_length=50, null=True)
    version_number = models.CharField("Version number ", max_length=50, null=True)
    is_permanent = models.BooleanField(default=False)
    product_grade = models.CharField(max_length=50, default="standard")
    product_stations = models.IntegerField(default=10000)

    allowed_ips = models.IntegerField(default=10)

    creation_date = models.DateTimeField("Date created ", null=True)
    expiration_date = models.DateTimeField("Expiration date ", null=True)

    def __str__(self):
        return self.product_name