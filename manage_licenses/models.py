from django.db import models

# Create your models here.
class License(models.Model):
    org_id = models.IntegerField(null=True)
    product_name = models.CharField(max_length=50)
    version = models.IntegerField(null=True)
    creator_address = models.CharField("Created by ", max_length=50)
    creation_date = models.DateTimeField("Date Created")

    def __str__(self):
        return self.product_name