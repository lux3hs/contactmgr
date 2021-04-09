
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# from manage_licenses.models import License

class Organization(models.Model):
    # org_id = id
    ORG_TYPE_CHOICES = [('customer', 'customer'), ('customer', 'partner')]
    org_type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES, null=True)
    org_name = models.CharField(max_length=50, unique=True)
    domain = models.CharField(max_length=50)

    def __str__(self):
        return self.org_name

    def get_table_dictionary(self):
        table_dict = {}
        table_dict["data_id"] = self.id
        table_dict["check_box"] = '<input type="checkbox" id="1" name="js-check-box" value="' + str(self.id) + '"  >'
        table_dict["org_type"] = self.org_type
        table_dict["org_name"] = self.org_name
        table_dict["domain"] = self.domain

        table_dict["empty_column"] = self.get_widget_template('empty_column')
        # table_dict["check_box"] = self.get_widget_template('check_box')
        table_dict["edit_button"] = self.get_widget_template('edit_button')
        table_dict["delete_button"] = self.get_widget_template('delete_button')
        return table_dict

    def get_widget_template(self, widget):
        if widget is "hello":
            greeting = "'hello world!'"
            widget_function = '<input type="button" class="button" onclick="console.log(' + greeting + ')" value="' + str(self.id) + '"/>'

        elif widget is "empty_column":
            widget_function = "<pre>    </pre>"

        elif widget is "edit_button":
            query_string = [self.id]
            name_link = "edit-org-data/" + str(query_string)
            widget_function = '<p><a class="button" href=' + '"' + name_link + '"' + '>Edit</a></p>'

        elif widget is "delete_button":
            delete_function = "deleteTableData(url='delete-org-selection', queryData=[" + str(self.id) + "], tableID='org-table')"
            widget_function = '<input type="button" class="button" onclick="' + delete_function + '" name="js-delete-button" value="Delete"/>'

        return widget_function

class Contact(models.Model):
    phone = models.IntegerField(null=True)
    creation_date = models.DateTimeField("Date Created", null=True)
    ROLE_CHOICES = [('admin', 'admin'), ('user', 'user')]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True)
    STATUS_CHOICES = [('active', 'active'), ('removed', 'removed')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=True)

    page_tab = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username

    def get_table_dictionary(self):
        table_dict = {}
        table_dict["data_id"] = self.id
        # table_dict["check_box"] = '<input type="checkbox" id="1" name="js-check-box" value="' + str(self.id) + '"  >'
        table_dict["username"] = self.user.username
        table_dict["first_name"] = self.user.first_name
        table_dict["last_name"] = self.user.last_name
        table_dict["email"] = self.user.email
        table_dict["contact_id"] = self.id
        table_dict["role"] = self.role
        table_dict["status"] = self.status
        table_dict["org_id"] = self.organization.id
        table_dict["org_name"] = self.organization.org_name

        table_dict["empty_column"] = self.get_widget_template('empty_column')
        table_dict["check_box"] = self.get_widget_template('check_box')
        table_dict["edit_button"] = self.get_widget_template('edit_button')
        table_dict["delete_button"] = self.get_widget_template('delete_button')

        return table_dict

    def get_widget_template(self, widget):
        if widget is "hello":
            greeting = "'hello world!'"
            widget_function = '<input type="button" class="button" onclick="console.log(' + greeting + ')" value="' + str(self.id) + '"/>'

        elif widget is "empty_column":
            widget_function = "<pre>    </pre>"


        elif widget is "check_box":
            widget_function = '<input type="checkbox" name="js-check-box" value="' + str(self.id) + '"/>'

        elif widget is "edit_button":
            query_string = [self.id]
            name_link = "edit-contact-data/" + str(query_string)
            widget_function = '<p><a class="button" href=' + '"' + name_link + '"' + '>Edit</a></p>'

        elif widget is "delete_button":
            delete_function = "deleteTableData(url='delete-contact-selection', queryData=[" + str(self.id) + "], tableID='contact-table')"
            widget_function = '<input type="button" class="button" onclick="' + delete_function + '" name="js-delete-button" value="Delete"/>'

        return widget_function

@receiver(post_save, sender=User)
def create_or_update_user_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(user=instance)
    instance.contact.save()
    

class Product(models.Model):
    product_name = models.CharField(max_length=50, null=True)
    product_version = models.CharField(max_length=50, null=True)
    GRADE_CHOICES = [('standard', 'standard'), ('enterprise', 'enterprise')]
    product_grade = models.CharField(max_length=50, choices=GRADE_CHOICES, default="standard", null=True)

    def __str__(self):
        return self.product_name + " v" + self.product_version

    def get_table_dictionary(self):
        table_dict = {}
        table_dict["data_id"] = self.id
        table_dict["check_box"] = '<input type="checkbox" id="1" name="js-check-box" value="' + str(self.id) + '"  >'
        table_dict["product_name"] = self.product_name
        table_dict["product_version"] = self.product_version

        table_dict["empty_column"] = self.get_widget_template("empty_column")
        table_dict["edit_button"] = self.get_widget_template('edit_button')
        table_dict["delete_button"] = self.get_widget_template("delete_button")
        return table_dict

    def get_widget_template(self, widget):
        if widget is "empty_column":
            widget_function = "<pre>    </pre>"

        elif widget is "edit_button":
            query_string = [self.id]
            name_link = "edit-product-data/" + str(query_string)
            widget_function = '<p><a class="button" href=' + '"' + name_link + '"' + '>Edit</a></p>'

        elif widget is "delete_button":
            delete_function = "deleteTableData(url='delete-product-selection', queryData=[" + str(self.id) + "], tableID='product-table')"
            widget_function = '<input type="button" class="button" onclick="' + delete_function + '" name="js-delete-button" value="Delete"/>'

        return widget_function
