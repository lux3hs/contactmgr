from django.db import models

# Create your models here.
class License(models.Model):
    """ License database model """
    org_name = models.CharField(max_length=50, null=True)
    org_id = models.IntegerField(default=0, null=True)
    entitlement_id = models.IntegerField(default=0, null=True)
    creator_email = models.CharField("Created by ", max_length=50, null=True)
    creator_phone = models.IntegerField(default=0, null=True)
    re_seller = models.CharField(max_length=50, null=True)
    product_name = models.CharField(max_length=50, null=True)
    version_number = models.CharField("Version number ", max_length=50, null=True)
    host_ip = models.CharField(max_length=50, null=True)
    is_permanent = models.BooleanField(default=True)
    product_grade = models.CharField(max_length=50, default="standard", null=True)
    product_stations = models.IntegerField(default=10000, null=True)
    allowed_ips = models.IntegerField(default=10, null=True)
    creation_date = models.DateField("Date created ", null=True)
    expiration_date = models.DateField("Expiration date ", null=True)

    # def get_model_fields(model):
    #     return model._meta.fields

    def get_table_dictionary(self):
        """ Get data for populating table """
        license_dict = {}
        license_dict["data_id"] = self.id
        license_dict["id"] = self.id
        license_dict["org_name"] = self.org_name
        license_dict["org_id"] = self.org_id
        license_dict["creator_email"] = self.creator_email
        license_dict["creator_phone"] = self.creator_phone
        license_dict["re_seller"] =self.re_seller
        license_dict["entitlement_id"] = self.entitlement_id
        license_dict["product_name"] = self.product_name
        license_dict["version_number"] = self.version_number
        license_dict["host_ip"] = self.host_ip
        license_dict["is_permanent"] = self.is_permanent
        license_dict["product_grade"] = self.product_grade
        license_dict["product_stations"] = self.product_stations
        license_dict["allowed_ips"] = self.allowed_ips
        license_dict["creation_date"] = str(self.creation_date)
        license_dict["expiration_date"] = str(self.expiration_date)

        return license_dict

    def get_package_data(self):
        """ Get data for generating license key """
        package_data = {}
        package_data["Org Name: "] = str(self.org_name)
        package_data["org ID: "] = str(self.org_id)
        package_data["Email: "] = str(self.creator_email)
        package_data["Phone: "] = str(self.creator_phone)
        package_data["Product: "] = str(self.product_name)
        package_data["Version: "] = str(self.version_number)
        package_data["Host IP: "] = str(self.host_ip)
        package_data["Permanent: "] = str(self.is_permanent)
        package_data["Grade: "] = str(self.product_grade)
        package_data["Stations: "] = str(self.product_stations)
        package_data["IPs: "] = str(self.allowed_ips)
        package_data["Created: "] = str(self.creation_date)
        package_data["Expires: "] = str(self.expiration_date)
        
        return package_data


    def __str__(self):
        return self.product_name