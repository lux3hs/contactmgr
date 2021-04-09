import datetime

from django.db import models

from .forms import LicenseCreationForm
from manage_contacts.models import Product, Organization

# Create your models here.
class License(models.Model):
    """ License database model """
    org_name = models.CharField(max_length=50, null=True)
    product_name = models.CharField(max_length=50, null=True)
    product_version = models.CharField(max_length=50, null=True)
    creator_email = models.CharField("Created by ", max_length=50, null=True)
    creator_phone = models.IntegerField(default=0, null=True)
    max_licenses = models.IntegerField(default=100)
    total_licenses = models.IntegerField(default=0)
    re_seller = models.CharField(max_length=50, null=True)
    host_ip = models.CharField(max_length=50, null=True)
    is_permanent = models.BooleanField(default=None, null=True)
    product_grade = models.CharField(max_length=50, default="standard", null=True)
    product_stations = models.IntegerField(default=0, null=True)
    allowed_ips = models.IntegerField(default=10, null=True)
    creation_date = models.DateTimeField("Date created ", null=True)
    expiration_date = models.DateTimeField("Expiration date ", null=True)

    is_master = models.BooleanField(default=None, null=True)

    def __str__(self):
        return str(self.org_name) + "-" + str(self.product_name)

    def get_table_dictionary(self):
        table_dict = {}
        table_dict["data_id"] = self.id
        table_dict["id"] = self.id
        table_dict["product_name"] = self.product_name
        table_dict["product_version"] = self.product_version
        table_dict["org_name"] = self.org_name
        table_dict["max_licenses"] = self.max_licenses
        table_dict["total_licenses"] = self.total_licenses
        num_allocated = str(self.total_licenses) + " of " + str(self.max_licenses)
        table_dict["num_allocated"] = num_allocated
        table_dict["creator_email"] = str(self.creator_email)
        table_dict["creator_phone"] = str(self.creator_phone)
        table_dict["host_ip"] = str(self.host_ip)
        table_dict["is_permanent"] = str(self.is_permanent)
        table_dict["product_grade"] = str(self.product_grade)
        table_dict["product_stations"] = str(self.product_stations)
        table_dict["allowed_ips"] = str(self.allowed_ips)
        table_dict["creation_date"] = self.creation_date.strftime('%m/%d/%Y')
        table_dict["expiration_date"] = self.expiration_date.strftime('%m/%d/%Y')


        table_dict["empty_column"] = self.get_widget_template('empty_column')
        # table_dict["name_link"] = self.get_widget_template('name_link')
        table_dict["check_box"] = self.get_widget_template('check_box')
        table_dict["radio_button"] = self.get_widget_template('radio_button')
        # table_dict["edit_button"] = self.get_widget_template('edit_button')
        table_dict["delete_button"] = self.get_widget_template('delete_button')
        table_dict["product_name_widget"] = self.get_widget_template('product_name_widget')
        table_dict["org_name_widget"] = self.get_widget_template('org_name_widget')
        table_dict["total_licenses_widget"] = self.get_widget_template('total_licenses_widget')
        table_dict["max_licenses_widget"] = self.get_widget_template('max_licenses_widget')
        table_dict["host_ip_widget"] = self.get_widget_template('host_ip_widget')
        table_dict["is_permanent_widget"] = self.get_widget_template('is_permanent_widget')
        table_dict["product_stations_widget"] = self.get_widget_template('product_stations_widget')
        table_dict["expiration_date_widget"] = self.get_widget_template('expiration_date_widget')

        table_dict["is_master_widget"] = self.get_widget_template('is_master_widget')


        return table_dict

    def get_widget_template(self, widget):
        if widget is "hello":
            greeting = "'hello world!'"
            widget_function = '<input type="button" class="button" onclick="console.log(' + greeting + ')" name="js-delete-button" value="' + str(self.id) + '"/>'

        elif widget is "empty_column":
            widget_function = "<pre>    </pre>"

        # elif widget is "name_link":
        #     name_link = "client-portal"
        #     widget_function = "<p><a href=" + '"' + name_link + '"' + ">" + self.product.product_name + "</a></p>"

        elif widget is "check_box":
            widget_function = '<input type="checkbox" name="license-check-box" value="' + str(self.id) + '">'

        elif widget is "radio_button":
            widget_function = '<input type="radio" name="license-radio-button" value="' + str(self.id) + '">'

        # elif widget is "edit_button":
        #     query_string = [self.id]
        #     name_link = "edit-entitlement-data/" + str(query_string)
        #     widget_function = '<p><a type="button" class="button" href=' + '"' + name_link + '"' + '>Edit</a></p>'

        elif widget is "delete_button":
            delete_function = "deleteTableData(url='delete-license-selection', queryData=[" + str(self.id) + "], tableID='license-table')"
            widget_function = '<input type="button" class="button" onclick="' + delete_function + '" name="js-delete-button" value="Delete"/>'

        elif widget is "org_name_widget":
            org_data = Organization.objects.all()
            org_string = ""
            for org in org_data:
                if org.org_name == self.org_name:
                    org_string += "<option value = " + str(org.id) + " selected>" + str(org.org_name) + "</option>"

                else:
                    org_string += "<option value = " + str(org.id) + ">" + str(org.org_name) + "</option>"

            widget_function = '<select name="org_id' + str(self.id) + '">' + org_string + '</select>'
  

        elif widget is "product_name_widget":
            product_data = Product.objects.all()
            product_string = ""
            for product in product_data:
                if product.product_name == self.product_name:
                    product_string += "<option value = " + str(product.product_name) + " selected>" + str(product.product_name) + "</option>"

                else:
                    product_string += "<option value = " + str(product.product_name) + ">" + str(product.product_name) + "</option>"

            widget_function = '<select name="product_name' + str(self.id) + '">' + product_string + '</select>'

        elif widget is "total_licenses_widget":
            widget_function = '<input type="number" name="total_licenses' + str(self.id) + '" value="' + str(self.total_licenses) + '">'

        elif widget is "max_licenses_widget":
            widget_function = '<input type="number" name="max_licenses' + str(self.id) + '" value="' + str(self.max_licenses) + '">'

        elif widget is "host_ip_widget":
            widget_function = '<input type="" name="host_ip' + str(self.id) + '" value="' + str(self.host_ip) + '">'

        elif widget is "is_permanent_widget":
            if self.is_permanent:
                widget_function = '<input type="checkbox" name="is_permanent' + str(self.id) + '" value="' + str(self.is_permanent) + '" checked>'

            else:
                widget_function = '<input type="checkbox" name="is_permanent' + str(self.id) + '" value="' + str(self.is_permanent) + '" >'

        elif widget is "is_master_widget":
            if self.is_master:
                widget_function = '<input type="checkbox" name="is_master' + str(self.id) + '" value="' + str(self.is_master) + '" checked>'

            else:
                widget_function = '<input type="checkbox" name="is_master' + str(self.id) + '" value="' + str(self.is_master) + '" >'

        elif widget is "product_stations_widget":
            widget_function = '<input type="number" name="product_stations' + str(self.id) + '" value="' + str(self.product_stations) + '">'

        elif widget is "expiration_date_widget":
            expiration_date = self.expiration_date.strftime("%Y-%m-%d")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            print(current_date)
            widget_function = '<input type="date" name="expiration_date' + str(self.id) + '" value="' + expiration_date + '" min="' + current_date + '">'

  
        return widget_function

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

    def check_trial(self):
        if self.is_permanent is True:
            return "TRIAL"

        else:
            return self.id

    def check_allocated_licenses(self):
        print(self.max_licenses)
        used_licenses = self.max_licenses - self.total_licenses
        if used_licenses < self.max_licenses:
            return True

        else:
            return False

    def subtract_license(self):
        if self.total_licenses > 0:
            self.total_licenses -= 1
            self.save()
            return True

        elif self.total_licenses == 0:
            return "no entitlements"

        else:
            return "number out of range"

    def add_license(self):
        if self.total_licenses < self.max_licenses:
            self.total_licenses += 1
            self.save()

            return True

        elif self.total_licenses == self.max_licenses:
            return "entitlements at max"

        else: 
            return "number out of range"