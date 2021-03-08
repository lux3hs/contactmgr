from django.db import models
import os
import subprocess
import datetime

class MasterLicense(models.Model):
    m_organizationName = models.CharField(max_length=200, default="N/A")
    m_IP_Host = models.CharField(max_length=200, default="N/A")
    m_emailAddress = models.EmailField(max_length=200, default="N/A")
    m_phoneNumber = models.CharField(max_length=200, default="N/A")
    m_user = models.CharField(max_length=200, default="N/A")
    m_textFile = models.CharField(max_length=200000, default="N/A")
    
    m_licenseType = models.CharField(max_length=200, default="N/A")
    m_licenseCreationTime = models.DateTimeField(auto_now_add=True)
    m_notes = models.CharField(max_length=200000, default="N/A")
    m_active = models.CharField(max_length=200, default="yes")
    m_reseller = models.CharField(max_length=500, default="N/A")

    def get_master_license_header(self):
        """
        Generates the header for the Master License File and returns based
        on the values of the current MasterLicense (self) object and returns the text
        """
        header_text  = "Master License ID: %d\n" % self.id
        header_text += "Organization Name: " + self.m_organizationName + "\n"
        header_text += "Organization Host/IP: " + self.m_IP_Host + "\n"
        header_text += "Email Address: " + self.m_emailAddress + "\n"
        header_text += "Phone Number: " + self.m_phoneNumber + "\n\n"
        return  header_text
    
    def get_master_key(self):
        """
        Generates the decoded MasterKey using the AlKeyMaker.exe encoder found in the
        bin folder. Returns an encoded String to be placed in the Master License File.
        """
        mkey = "masterip=" + self.m_IP_Host + "&masterid=%d" % self.id
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        outputFile = BASE_DIR + "/bin/output_string.txt"
        encrypt_command =   "\"" + BASE_DIR + "\\bin\\AlKeyMaker.exe\"  string=\"" +\
                            mkey + "\" outputfile=\"" + outputFile + "\""
        subprocess.call(encrypt_command)
        outputFile = BASE_DIR + "/bin/output_string.txt"
        f = open(outputFile, "r")
        result = f.read()
        coded_key = ""
        got_key = False
        if "Key=" in result:
            got_key = True
            coded_key = result[result.index("Key=")+ 4 : len(result)] 
        if got_key:
            return coded_key
        else:
            return ''

class ProductLicense(models.Model):
    masterLicense = models.ForeignKey(MasterLicense, on_delete=models.CASCADE)
    m_licType = models.CharField(max_length=50, default="N/A")
    m_host_IP = models.CharField(max_length=200, default="N/A")
    m_stations = models.IntegerField(default=0)
    m_ips = models.IntegerField(default=0)
    m_task = models.IntegerField(default=0)
    m_log = models.IntegerField(default=0)
    m_node = models.IntegerField(default=0)
    m_sys = models.IntegerField(default=0)
    m_snmp = models.IntegerField(default=0)
    m_startDate = models.IntegerField(default=0)
    m_endDate = models.IntegerField(default=0)
    m_supportID = models.CharField(max_length=200, default="N/A")
    m_expirationDate = models.IntegerField(default=0)
    m_lineNumber = models.IntegerField(default=0)         
    m_productName = models.CharField(max_length=200, default="N/A")
    m_productVersion = models.CharField(max_length=200, default="N/A")
    m_grade = models.CharField(max_length=200, default="N/A")
    m_permanent = models.IntegerField(default=0) 
    
    def __str__(self):
        """
        This function prints some values from the current ProductLicense object (self)
        It was used for testing.
        """
        plStr = ""
        plStr += self.m_productName
        plStr += " "
        plStr += self.m_productVersion
        plStr += " "
        if (self.m_permanent):
            plStr += "Permenant"
        else:
            plStr += "Leased"
        plStr += " "
        plStr += self.m_grade
        plStr += " "
        plStr += self.m_licType
        plStr += " "
        plStr += self.m_host_IP
        plStr += " "
        plStr += self.m_supportID
        plStr += " "
        plStr =  plStr + "%d" % self.m_startDate
        plStr += " "
        plStr =  plStr + "%d" %  self.m_endDate
        plStr += " "
        return plStr
    
    def get_product_clear_text_line_m(self):
        """
        This function Generates a clear text string to be placed in the Master License File.
        """
        product_key = "Product Name: " + self.m_productName 
        product_key += ", Host/IP address: " + self.m_host_IP 
        product_key += ", Version: " + self.m_productVersion
        if (self.m_productName.lower() == "apploader"):
            product_key += ", Num of rUsers: %d" % (self.m_stations)
        else:
            product_key += ", Num of stations: %d" % (self.m_stations)
        if (self.m_permanent):
            product_key += ", Permanent License "
        else:
            product_key +=  ", Lease Start Date: " + \
                            datetime.datetime.utcfromtimestamp(self.m_startDate).strftime("%m/%d/%Y %I:%M %p") + \
                            " (GMT)"
            product_key +=  ", Lease End Date: "+\
                            datetime.datetime.utcfromtimestamp(self.m_endDate).strftime("%m/%d/%Y %I:%M %p") + \
                            " (GMT)"
        if  (self.m_productName.lower() == "apploader") or\
            (self.m_productName.lower() == "appswatch") or\
            (self.m_productName.lower() == "backend"):
            
            product_key += ", Number of IPs:%d" % (self.m_ips)
            product_key +=  ", Task Limit :%d, Log Limit: %d, Node Limit: %d" %\
                            (self.m_task, self.m_log, self.m_node)
            product_key +=  ", System Limit: %d, SNMP Limit: %d" %\
                            (self.m_sys, self.m_snmp)
        product_key += ", Grade:" + self.m_grade
        product_key += ", User name: all"
        product_key += ", Support ID: " + self.m_supportID
        product_key += ", Support Expiration Date: " + \
                    datetime.datetime.fromtimestamp(self.m_expirationDate).strftime("%m/%d/%Y %H:%M")
        return product_key
    
    def get_product_clear_text_line_s(self):
        """
        This function Generates a clear text string to be placed in the Single License File.
        """
        product_key = "Product Name: " + self.m_productName 
        product_key += "\nHost/IP address: " + self.m_host_IP 
        product_key += "\nVersion: " + self.m_productVersion
        if (self.m_productName.lower() == "apploader"):
            product_key += "\nNum of rUsers: %d" % (self.m_stations)
        else:
            product_key += "\nNum of stations: %d" % (self.m_stations)
        if (self.m_permanent):
            product_key += "\nPermanent License "
        else:
            product_key +=  "\nLease Start Date: " + \
                            datetime.datetime.utcfromtimestamp(self.m_startDate).strftime("%m/%d/%Y %I:%M %p") 
            product_key += " (GMT)"
            product_key +=  "\nLease End Date: "+\
                            datetime.datetime.utcfromtimestamp(self.m_endDate).strftime("%m/%d/%Y %I:%M %p")
            product_key += " (GMT)"
        if  (self.m_productName.lower() == "apploader") or\
            (self.m_productName.lower() == "appswatch") or\
            (self.m_productName.lower() == "backend"):
            
            product_key += "\nNumber of IPs:%d" % (self.m_ips)
            product_key +=  "\nTask Limit :%d, Log Limit: %d, Node Limit: %d" %\
                            (self.m_task, self.m_log, self.m_node)
            product_key +=  "\nSystem Limit: %d, SNMP Limit: %d" %\
                            (self.m_sys, self.m_snmp)
        product_key += "\nGrade:" + self.m_grade
        product_key += "\nUser name: all"
        product_key += "\nSupport ID: " + self.m_supportID
        product_key += "\nSupport Expiration Date: " + \
                    datetime.datetime.utcfromtimestamp(self.m_expirationDate).strftime("%m/%d/%Y %I:%M %p")
        product_key += " (GMT)"
        return product_key
    
    def get_product_key(self, organization = "NRG Global Inc."):
        """
        Generates the decoded ProductKey using the AlKeyMaker.exe encoder found in the
        bin folder. Returns an encoded String to be placed in the Master License File.
        """
        product_key = "organization=" + organization + "&product=" + self.m_productName +\
                        "&Ip address="
        product_key += self.m_host_IP + "&Hostname=" + self.m_host_IP + "&Version=" +\
                        self.m_productVersion
        product_key += "&Num of stations=%d&ips=%d&License Start Date=%d" %\
                        (self.m_stations, self.m_ips, self.m_startDate)
        product_key += "&License End Date=%d&task=%d&log=%d&node=%d" %\
                        (self.m_endDate, self.m_task, self.m_log, self.m_node)
        product_key += "&system=%d&snmp=%d&grade=" % (self.m_sys, self.m_snmp)
        product_key += self.m_grade + "&sid=" + self.m_supportID +\
                        "&expdate=%d&username=all" % (self.m_expirationDate)
        if (self.m_productName != "Backend" and
            self.m_productName != "AppLoader" and
            self.m_productName != "AppsWatch"):
            product_key += "&end=true"
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        outputFile = BASE_DIR + "/bin/output_string1.txt"
        encrypt_command = "\"" + BASE_DIR + "\\bin\\AlKeyMaker.exe\"  string=\"" +\
                            product_key + "\" outputfile=\"" + outputFile + "\""
        subprocess.call(encrypt_command)
        outputFile = BASE_DIR + "/bin/output_string1.txt"
        f = open(outputFile, "r")
        result = f.read()
        coded_key = ""
        got_key = False
        if "Key=" in result:
            got_key = True
            coded_key = result[result.index("Key=") + 4 : len(result)]
        if got_key:
            return coded_key
        else:
            return ''          
        return product_key