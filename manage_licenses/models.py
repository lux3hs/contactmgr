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

    def get_license_dictionary(self):
        license_dict = {}
        license_dict["Org"] = self.org_name
        license_dict["OrgID"] = self.org_id
        license_dict["EntID"] = self.entitlement_id 
        license_dict["IP Host"] = self.IP_Host
        license_dict["Email"] = self.creator_email     
        license_dict["Product"] = self.product_name 
        license_dict["Version"] = self.version_number
        license_dict["Permanent"] = self.is_permanent
        license_dict["Grade"] = self.product_grade
        license_dict["Stations"] = self.product_stations
        license_dict["IPs"] = self.allowed_ips
        license_dict["Created"] = self.creation_date
        license_dict["Expires"] = self.expiration_date

        return license_dict

    def __str__(self):
        return self.product_name