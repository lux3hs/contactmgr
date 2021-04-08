from django.db import models

# Create your models here.
class License(models.Model):
    """ License database model """
    org_name = models.CharField(max_length=50, null=True)
    product_name = models.CharField(max_length=50, null=True)
    product_version = models.CharField(max_length=50, null=True)
    creator_email = models.CharField("Created by ", max_length=50, null=True)
    creator_phone = models.IntegerField(default=0, null=True)
    re_seller = models.CharField(max_length=50, null=True)
    host_ip = models.CharField(max_length=50, null=True)
    is_permanent = models.BooleanField(default=None, null=True)
    product_grade = models.CharField(max_length=50, default="standard", null=True)
    product_stations = models.IntegerField(default=0, null=True)
    allowed_ips = models.IntegerField(default=10, null=True)
    creation_date = models.DateTimeField("Date created ", null=True)
    expiration_date = models.DateTimeField("Expiration date ", null=True)

    def __str__(self):
        return str(self.org_name) + "-" + str(self.product_name)

    def check_trial(self):
        if self.is_permanent is True:
            return "TRIAL"

        else:
            return self.id

    def get_license_header(self):
        """ Get header for displaying in license key """
        creation_date = self.creation_date.strftime("%m/%d/%Y %I:%M %p")
        expiration_date = self.expiration_date.strftime("%m/%d%Y %I:%M %p")
        package_data = {}
        package_data["Product Name: "] = str(self.product_name)
        package_data["Host/IP address: "] = str(self.host_ip)
        package_data["Version: "] = str(self.product_version)
        package_data["Num of stations: "] = str(self.product_stations)
        package_data["Lease Start Date: "] = str(creation_date)
        package_data["Lease End Date: "] = str(expiration_date)
        package_data["Grade: "] = str(self.product_grade)
        package_data["User name: "] = str(self.creator_email)
        package_data["Support ID: "] = self.check_trial()
        package_data["Support Expiration Date: "] = str(expiration_date)
        return package_data

    def get_key_string(self):
        organization = self.org_name
        
        task = 0
        log = 0
        node = 0
        system = 0
        snmp = 0

        creation_date = self.creation_date
        expiration_date = self.expiration_date
        crt_date_utc = creation_date.timestamp()
        exp_date_utc = expiration_date.timestamp()

        product_key = "organization=" + str(organization)
        product_key += "&product=" + self.product_name
        product_key += "&Ip address=" + str(self.host_ip)
        product_key += "&Hostname=" + str(self.host_ip)
        product_key += "&Version=" + str(self.product_version)
        product_key += "&Num of stations=" + str(self.product_stations)
        product_key += "&ips=" + str(self.allowed_ips)
        product_key += "&License Start Date=" + str(crt_date_utc)
        product_key += "&License End Date=" + str(exp_date_utc)
        product_key += "&task=" + str(task)
        product_key += "&log=" + str(log)
        product_key += "&node=" + str(node)
        product_key += "&system=" + str(system)
        product_key += "&snmp=" + str(snmp)
        product_key += "&grade=" + str(self.product_grade)
        product_key += "&sid=" + str(self.id)
        product_key += "&expdate=" + str(exp_date_utc)
        product_key += "&username=all"

        if (self.product_name is not "Backend" and
            self.product_name is not "AppLoader" and
            self.product_name is not "AppsWatch"):
            product_key += "&end=true"

        return product_key