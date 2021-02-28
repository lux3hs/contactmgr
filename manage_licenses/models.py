from django.db import models

# Create your models here.
class License(models.Model):
    """ License database model """
    org_id = models.IntegerField(default=0, null=True)
    product_name = models.CharField(max_length=50, null=True)
    version_number = models.CharField("Version number ", max_length=50, null=True)
    creator_address = models.CharField("Created by ", max_length=50, null=True)
    creation_date = models.DateTimeField("Date created ", null=True)

    def __str__(self):
        return self.product_name