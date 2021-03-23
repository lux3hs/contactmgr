from django.db import models

# Create your models here.
class License(models.Model):
    """ License database model """
    org_name = models.CharField(max_length=50, null=True)
    org_id = models.IntegerField(default=0, null=True)
    entitlement_id = models.IntegerField(default=0, null=True)
    IP_Host = models.CharField(max_length=50, null=True)
    creator_email = models.CharField("Created by ", max_length=50, null=True)
    
    product_name = models.CharField(max_length=50, null=True)
    version_number = models.CharField("Version number ", max_length=50, null=True)
    is_permanent = models.BooleanField(default=True)
    product_grade = models.CharField(max_length=50, default="standard")
    product_stations = models.IntegerField(default=10000)

    allowed_ips = models.IntegerField(default=10)

    creation_date = models.DateTimeField("Date created ", null=True)
    expiration_date = models.DateTimeField("Expiration date ", null=True)

    def get_table_dictionary(self):
        license_dict = {}
        license_dict["data_id"] = self.id
        license_dict["org_name"] = self.org_name
        license_dict["org_id"] = self.org_id
        license_dict["entitlement_id"] = self.entitlement_id
        license_dict["IP_Host"] = self.IP_Host
        license_dict["creator_email"] = self.creator_email
        license_dict["product_name"] = self.product_name
        license_dict["version_number"] = self.version_number
        license_dict["is_permanent"] = self.is_permanent
        license_dict["product_grade"] = self.product_grade
        license_dict["product_stations"] = self.product_stations
        license_dict["allowed_ips"] = self.allowed_ips
        license_dict["creation_date"] = self.creation_date
        license_dict["expiration_date"] = self.expiration_date

        return license_dict

    # def get_user_licenses(self, current_user):
    #     org_id = current_user.organization.id
    #     user_licenses = self.filter(org_id=org_id)
    #     return user_licenses

        



    def __str__(self):
        return self.product_name