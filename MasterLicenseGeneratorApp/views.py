from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
import json, logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from MasterLicenseGeneratorApp.models import MasterLicense
from MasterLicenseGeneratorApp.models import ProductLicense
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import calendar
import datetime
import os

from .forms import SearchForm, ChoiceForm, SaveLicenseForm

from manage_contacts.models import Contact, Entitlement, Organization




@login_required
def generate_licenses(request):
    # product_form = ChoiceForm()
    # search_form = SearchForm()
    # save_license_form = SaveLicenseForm()
    current_user = request.user
    user_id = current_user.id
    user_email = current_user.email
    contact_data = Contact.objects.filter(user_id=user_id).get()
    user_role = contact_data.role
    org_id = contact_data.organization_id
    org_data = Organization.objects.filter(id=org_id).get()
    user_org = org_data.org_name

    product_entitlements = Entitlement.objects.filter(organization_id=org_id)
    print(product_entitlements)

    master_licenses = MasterLicense.objects.filter(m_organizationName=user_org)
    print(master_licenses)


    if request.method == "POST":


        #Build master license object
        ml = MasterLicense()

        #Add field values to master license
        ml.m_licenseType = "Master License"
        ml.m_organizationName = request.POST.get('orgname', '')
        ml.m_emailAddress = request.POST.get('email', '')
        ml.m_phoneNumber = request.POST.get('phone', '')
        tmp_master_license_host_ip = request.POST.get('iphost', '')
        ml.m_IP_Host = tmp_master_license_host_ip.strip()
        #ml.m_notes = request.POST.get('notes', '')
        ml.m_reseller =  request.POST.get('reseller', '')
        ml.save()

        cleartextheader = ml.get_master_license_header()
        
        codedKeysText = ""
        # codedKeysText += "MKey=" + ml.get_master_key() + "\n"
        codeKeysText = "MKey = thisKey \n"

        #Set field values
        grades = request.POST.get('grade', '')
        grade_arr = grades.split(';')
        grade_arr.pop()
        
        start_dates = request.POST.get('sd', '')
        start_date_arr = start_dates.split(';')
        start_date_arr.pop()
        
        end_dates = request.POST.get('ed', '')
        end_date_arr = end_dates.split(';')
        end_date_arr.pop()
        
        exp_dates = request.POST.get('exd', '')
        exp_date_arr = exp_dates.split(';')
        exp_date_arr.pop()

        support_ids = request.POST.get('sid', '')
        support_id_arr = support_ids.split(';')
        support_id_arr.pop()
        
        license_types = request.POST.get('perm', '')
        license_type_arr = license_types.split(';')
        license_type_arr.pop()
        
        number_ips = request.POST.get('ips', '')
        number_ips_arr = number_ips.split(';')
        number_ips_arr.pop()
        
        hostips_allowed = request.POST.get('hip', '')
        hostip_allowed_arr = hostips_allowed.split(';')
        hostip_allowed_arr.pop()
        
        logs = request.POST.get('log', '')
        log_arr = logs.split(';')
        log_arr.pop()
        
        tasks = request.POST.get('task', '')
        task_arr = tasks.split(';')
        task_arr.pop()
        
        nodes = request.POST.get('node', '')
        node_arr = nodes.split(';')
        node_arr.pop()
        
        systems = request.POST.get('sys', '')
        system_arr = systems.split(';')
        system_arr.pop()
        
        snmps = request.POST.get('snmp', '')
        snmp_arr = snmps.split(';')
        snmp_arr.pop()
        
        names = request.POST.get('name', '')
        product_name_arr = names.split(';')
        product_name_arr.pop()
        
        versions = request.POST.get('vers', '')
        product_vers_arr = versions.split(';')
        product_vers_arr.pop()
        
        num_stations = request.POST.get('station', '')
        num_stations_arr = num_stations.split(';')
        num_stations_arr.pop()
        for i in range (0, len(num_stations_arr)):
            print(i)
            clearTextLicenseLine = ""
            codedKeysLine = "Key%d="%i
            pl = ProductLicense()
            pl.masterLicense = ml
            
            tmp_product_allowed_host_ip = hostip_allowed_arr[i]
            pl.m_host_IP = tmp_product_allowed_host_ip.strip()
            
            pl.m_stations = int(num_stations_arr[i])
            pl.m_ips = int(number_ips_arr[i])
            pl.m_task = int(task_arr[i])
            pl.m_log = int(log_arr[i])
            pl.m_node = int(node_arr[i])
            pl.m_sys = int(system_arr[i])
            pl.m_snmp = int(snmp_arr[i])
            pl.m_supportID = support_id_arr[i]
            pl.m_expirationDate = round(calendar.timegm(datetime.datetime.strptime(exp_date_arr[i], "%Y-%m-%d %H:%M:%S").timetuple()))
            pl.m_productName = product_name_arr[i]
            pl.m_productVersion = product_vers_arr[i]
            pl.m_grade = grade_arr[i]
            if (license_type_arr[i]=="true"):
                pl.m_permanent = 1
                pl.m_startDate = 0
                pl.m_endDate = 0
            else:
                pl.m_permanent = 0
                pl.m_startDate = round(calendar.timegm(datetime.datetime.strptime(start_date_arr[i], "%Y-%m-%d %H:%M:%S").timetuple()))
                pl.m_endDate = round(calendar.timegm(datetime.datetime.strptime(end_date_arr[i], "%Y-%m-%d %H:%M:%S").timetuple()))
            pl.m_lineNumber = i
            if (hostip_allowed_arr[i] == "token") or (hostip_allowed_arr[i] == "token24"):
                pl.m_licType = hostip_allowed_arr[i]
            else:
                pl.m_licType = "normal"      
            pl.save()
            clearTextLicenseLine += pl.get_product_clear_text_line_m()
            codedKeysLine += pl.get_product_key(ml.m_organizationName) + "\n"
            clearTextLicenseLine += "\n"
            cleartextheader += clearTextLicenseLine
            codedKeysText += codedKeysLine
        cleartextheader += "\n\n"
        cleartextheader += codedKeysText
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        outputFile = BASE_DIR + "/bin/licenseserver.lic"
        f = open(outputFile, "w")
        f.write(cleartextheader)
        final_data = {}
        final_data['success'] = True
        ml.m_textFile = cleartextheader
        ml.m_user = request.user.get_username()
        ml.save()
        logging.info("User: " + str(request.user.username) + 
                    " has created Master License #: " + str(ml.id))
        # return HttpResponse(json.dumps(final_data), content_type="application/json")

        # context = final_data
        print(final_data)
        search_form = SearchForm()
        save_license_form = SaveLicenseForm()
        context = {'search_form':search_form, 'save_license_form':save_license_form}

        return render(request, 'MasterLicenseGeneratorApp/generate-licenses.html', context=context)

    else:

        search_form = SearchForm()
        save_license_form = SaveLicenseForm()
        context = {'search_form':search_form, 
                   'save_license_form':save_license_form, 
                   'product_entitlements':product_entitlements, 
                   'master_licenses':master_licenses}

        return render(request, 'MasterLicenseGeneratorApp/generate-licenses.html', context=context)





@login_required
def ml_new(request):
    return render(request, 'MasterLicenseGeneratorApp/generate-licenses.html', {'ml_id':0})


@login_required
def render_record(request, ml_id):
    return render(request, 'MasterLicenseGeneratorApp/generate-licenses.html', {'ml_id':ml_id})

@login_required
def ml_list(request):
    return render(request, 'license_reports.html')




@login_required
def ml_return_list(request):
    """ Returns a json of current master licenses """
    final_data = {}
    master_detail = []
    final_data['success'] = False
    
    orderBy = "-id"
    if("order_by" in request.GET):
        orderBy = request.GET.get('order_by', '')
    
    # master_license_list = MasterLicense.objects.order_by(orderBy)

    if("filter_by" in request.GET and 
        "filter_value" in request.GET):
        filterBy = request.GET.get('filter_by', '')
        filterValue = request.GET.get('filter_value', '')
        # if (filterBy == "Organization"):
        if (filterBy == "organization"):
            master_license_list = MasterLicense.objects.order_by(orderBy).filter(m_organizationName__contains=filterValue)[:25]
        # elif (filterBy == "Host/IP"):
        elif (filterBy == "hostip"):
            master_license_list = MasterLicense.objects.order_by(orderBy).filter(m_IP_Host__contains=filterValue)[:25]
        # elif (filterBy == "Email"):
        elif (filterBy == "email"):
            master_license_list = MasterLicense.objects.order_by(orderBy).filter(m_emailAddress__contains=filterValue)[:25]
        # elif (filterBy == "Phone"):
        elif (filterBy == "phone"):
            master_license_list = MasterLicense.objects.order_by(orderBy).filter(m_phoneNumber__contains=filterValue)[:25]
        # elif (filterBy == "Username"):
        elif (filterBy == "username"):
            master_license_list = MasterLicense.objects.order_by(orderBy).filter(m_user__contains=filterValue)[:25]
        # elif (filterBy == "product"):
            # product_detail_list = ProductLicense.objects.order_by(orderBy).filter(m_productName=filterValue)[:25]
            # if product_detail_list:
                # product = product_detail_list[0]
                # temp_master_detail = {}
                # if product:
                    # temp_master_detail['product']    = productNameShortcut(product.m_productName)
                    # temp_master_detail['version']    = product.m_productVersion
                    # temp_master_detail['stations']   = product.m_stations
                    # if product.m_permanent:
                        # temp_master_detail['duration'] = "FULL"
                    # else:
                        # temp_master_detail['duration'] = "EVAL"
                        
            # master_detail.append(temp_master_detail)                
    else:
        master_license_list = MasterLicense.objects.order_by(orderBy)[:25]

    if master_license_list:
        for master_license in master_license_list:
            if master_license:
                final_data['success'] = True
                temp_master_detail = {}
                temp_master_detail['mid']          = master_license.id
                temp_master_detail['user']         = master_license.m_user
                temp_master_detail['hostip']       = master_license.m_IP_Host
                temp_master_detail['organization'] = master_license.m_organizationName
                #temp_master_detail['email']        = master_license.m_emailAddress
                #temp_master_detail['phone']        = master_license.m_phoneNumber
                temp_master_detail['cdate']        = calendar.timegm(master_license.m_licenseCreationTime.timetuple())
                temp_master_detail['type']      = master_license.m_licenseType.partition(' ')[0]
                temp_master_detail['active']     = master_license.m_active
                
                temp_master_detail['product']      = ""
                temp_master_detail['version']      = ""
                temp_master_detail['stations']     = ""
                temp_master_detail['duration']     = ""
                product_detail_list = ProductLicense.objects.filter(masterLicense_id = master_license.id)
                if product_detail_list:
                    product = product_detail_list[0]
                    if product:
                        temp_master_detail['product']     = productNameShortcut(product.m_productName)
                        temp_master_detail['version']    = product.m_productVersion
                        temp_master_detail['stations']    = product.m_stations
                        if product.m_permanent:
                            temp_master_detail['duration'] = "FULL"
                        else:
                            temp_master_detail['duration'] = "EVAL"
                            
                master_detail.append(temp_master_detail)
    final_data['totalCount'] = len(master_detail)
    # pageNumber = request.GET.get('page', '')
    # paginator = Paginator(master_detail, 25)
    # try:
        # final_data['data'] = paginator.page(pageNumber).object_list
    # except PageNotAnInteger:
    #   # If page is not an integer, deliver first page.
        # final_data['data'] = paginator.page(1).object_list
    # except EmptyPage:
    #   # If page is out of range (e.g. 9999), deliver last page of results.
        # final_data['data'] = paginator.page(paginator.num_pages).object_list
    final_data['data'] = master_detail
    # return HttpResponse(json.dumps(final_data), content_type="application/json")

    context = final_data
    print(context)
    return render(request, 'MasterLicenseGeneratorApp/generate-licenses.html', context=context)



def productNameShortcut(productName):
    productName="scenariobuilder"
    if productName.lower() == "scenariobuilder":
        return "SB"
    elif productName.lower() == "apploader":
        return "AL"
    elif productName.lower() == "appswatch":
        return "AW"
    elif productName.lower() == "appverify":
        return "AV"
    elif productName.lower() == "scenariostation":
        return "SS"
    elif productName.lower() == "rtester":
        return "RT"
    elif productName.lower() == "backend":
        return "BE"
    return productName


    
@csrf_exempt
def ml_load_record(request, ml_id=1):
    """ Pass in master license id to retrieve record """

    my_var = False
    # if not request.user.is_authenticated():
    if my_var == True:
        return redirect('Master_License_Generator.views.login')
    else: 
        final_data = {}
        temp_data = {}
        master_detail = {}
        product_detail = []
        final_data['success'] = False

        master_license = MasterLicense.objects.get(id=ml_id)
        
        if master_license:   
            master_detail['hostip']       = master_license.m_IP_Host
            master_detail['organization'] = master_license.m_organizationName
            master_detail['email']        = master_license.m_emailAddress
            master_detail['phone']        = master_license.m_phoneNumber
            master_detail['notes']        = master_license.m_notes
            master_detail['active']       = master_license.m_active
            master_detail['reseller']     = master_license.m_reseller

        product_detail_list = ProductLicense.objects.filter(masterLicense_id = ml_id)
        valid_list = False
        if product_detail_list:
            for product in product_detail_list:
                if product:
                    valid_list = True
                    temp_product_detail = {}
                    temp_product_detail['program']    = product.m_productName
                    temp_product_detail['version']    = product.m_productVersion
                    temp_product_detail['license']    = product.m_permanent
                    temp_product_detail['hostip']     = product.m_host_IP
                    temp_product_detail['stations']   = product.m_stations
                    temp_product_detail['ipnumber']   = product.m_ips
                    temp_product_detail['tasks']      = product.m_task
                    temp_product_detail['logs']       = product.m_log
                    temp_product_detail['nodes']      = product.m_node
                    temp_product_detail['systems']    = product.m_sys
                    temp_product_detail['snmps']      = product.m_snmp
                    temp_product_detail['sdate']      = product.m_startDate
                    temp_product_detail['edate']      = product.m_endDate
                    temp_product_detail['grades']     = product.m_grade
                    temp_product_detail['sids']       = product.m_supportID
                    temp_product_detail['expdate']    = product.m_expirationDate
                    product_detail.append(temp_product_detail)

        #everytime you get something from database
        if master_license or valid_list:
            final_data['success'] = True
            temp_data['master'] = master_detail
            temp_data['product'] = product_detail
            final_data['data'] = temp_data

        return HttpResponse(json.dumps(final_data), content_type="application/json")

@csrf_exempt
def save_license_to_db(request):
    """ Add master license to database """

    #Build master license object
    ml = MasterLicense()

    #Add field values to master license
    ml.m_licenseType = "Master License"
    ml.m_organizationName = request.POST.get('orgname', '')
    ml.m_emailAddress = request.POST.get('email', '')
    ml.m_phoneNumber = request.POST.get('phone', '')
    tmp_master_license_host_ip = request.POST.get('iphost', '')
    ml.m_IP_Host = tmp_master_license_host_ip.strip()
    #ml.m_notes = request.POST.get('notes', '')
    ml.m_reseller =  request.POST.get('reseller', '')
    ml.save()

    cleartextheader = ml.get_master_license_header()
    
    codedKeysText = ""
    # codedKeysText += "MKey=" + ml.get_master_key() + "\n"
    codeKeysText = "MKey = thisKey \n"

    #Set field values
    grades = request.POST.get('grade', '')
    grade_arr = grades.split(';')
    grade_arr.pop()
    
    start_dates = request.POST.get('sd', '')
    start_date_arr = start_dates.split(';')
    start_date_arr.pop()
    
    end_dates = request.POST.get('ed', '')
    end_date_arr = end_dates.split(';')
    end_date_arr.pop()
    
    exp_dates = request.POST.get('exd', '')
    exp_date_arr = exp_dates.split(';')
    exp_date_arr.pop()

    support_ids = request.POST.get('sid', '')
    support_id_arr = support_ids.split(';')
    support_id_arr.pop()
    
    license_types = request.POST.get('perm', '')
    license_type_arr = license_types.split(';')
    license_type_arr.pop()
    
    number_ips = request.POST.get('ips', '')
    number_ips_arr = number_ips.split(';')
    number_ips_arr.pop()
    
    hostips_allowed = request.POST.get('hip', '')
    hostip_allowed_arr = hostips_allowed.split(';')
    hostip_allowed_arr.pop()
    
    logs = request.POST.get('log', '')
    log_arr = logs.split(';')
    log_arr.pop()
    
    tasks = request.POST.get('task', '')
    task_arr = tasks.split(';')
    task_arr.pop()
    
    nodes = request.POST.get('node', '')
    node_arr = nodes.split(';')
    node_arr.pop()
    
    systems = request.POST.get('sys', '')
    system_arr = systems.split(';')
    system_arr.pop()
    
    snmps = request.POST.get('snmp', '')
    snmp_arr = snmps.split(';')
    snmp_arr.pop()
    
    names = request.POST.get('name', '')
    product_name_arr = names.split(';')
    product_name_arr.pop()
    
    versions = request.POST.get('vers', '')
    product_vers_arr = versions.split(';')
    product_vers_arr.pop()
    
    num_stations = request.POST.get('station', '')
    num_stations_arr = num_stations.split(';')
    num_stations_arr.pop()
    for i in range (0, len(num_stations_arr)):
        print(i)
        clearTextLicenseLine = ""
        codedKeysLine = "Key%d="%i
        pl = ProductLicense()
        pl.masterLicense = ml
        
        tmp_product_allowed_host_ip = hostip_allowed_arr[i]
        pl.m_host_IP = tmp_product_allowed_host_ip.strip()
        
        pl.m_stations = int(num_stations_arr[i])
        pl.m_ips = int(number_ips_arr[i])
        pl.m_task = int(task_arr[i])
        pl.m_log = int(log_arr[i])
        pl.m_node = int(node_arr[i])
        pl.m_sys = int(system_arr[i])
        pl.m_snmp = int(snmp_arr[i])
        pl.m_supportID = support_id_arr[i]
        pl.m_expirationDate = round(calendar.timegm(datetime.datetime.strptime(exp_date_arr[i], "%Y-%m-%d %H:%M:%S").timetuple()))
        pl.m_productName = product_name_arr[i]
        pl.m_productVersion = product_vers_arr[i]
        pl.m_grade = grade_arr[i]
        if (license_type_arr[i]=="true"):
            pl.m_permanent = 1
            pl.m_startDate = 0
            pl.m_endDate = 0
        else:
            pl.m_permanent = 0
            pl.m_startDate = round(calendar.timegm(datetime.datetime.strptime(start_date_arr[i], "%Y-%m-%d %H:%M:%S").timetuple()))
            pl.m_endDate = round(calendar.timegm(datetime.datetime.strptime(end_date_arr[i], "%Y-%m-%d %H:%M:%S").timetuple()))
        pl.m_lineNumber = i
        if (hostip_allowed_arr[i] == "token") or (hostip_allowed_arr[i] == "token24"):
            pl.m_licType = hostip_allowed_arr[i]
        else:
            pl.m_licType = "normal"      
        pl.save()
        clearTextLicenseLine += pl.get_product_clear_text_line_m()
        codedKeysLine += pl.get_product_key(ml.m_organizationName) + "\n"
        clearTextLicenseLine += "\n"
        cleartextheader += clearTextLicenseLine
        codedKeysText += codedKeysLine
    cleartextheader += "\n\n"
    cleartextheader += codedKeysText
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    outputFile = BASE_DIR + "/bin/licenseserver.lic"
    f = open(outputFile, "w")
    f.write(cleartextheader)
    final_data = {}
    final_data['success'] = True
    ml.m_textFile = cleartextheader
    ml.m_user = request.user.get_username()
    ml.save()
    logging.info("User: " + str(request.user.username) + 
                 " has created Master License #: " + str(ml.id))
    # return HttpResponse(json.dumps(final_data), content_type="application/json")

    context = final_data
    print(context)
    return render(request, 'MasterLicenseGeneratorApp/generate-licenses.html', context=context)

@csrf_exempt
def save_license_active_status_to_db(request, ml_id=0):
    my_var=True
    # if not request.user.is_authenticated():
    if my_var == False:
        return redirect('Master_License_Generator.views.login')
    else:
        final_data = {}
        final_data['success'] = False
        try:
            master_license = MasterLicense.objects.get(id=ml_id)
            master_license.m_active = request.POST.get('active', '')
            master_license.save()
            logging.info("User: " + str(request.user.username) + 
                     " has updated Master License active status #: " + 
                     str(master_license.id) + " " + str(master_license.m_active))
            final_data['success'] = True
        except Exception as exp:
            logging.info(" ERROR:" + str(exp))
        return HttpResponse(json.dumps(final_data), content_type="application/json")

def download_master_license_file(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    licenseFile = BASE_DIR + "/bin/licenseserver.lic"
    f = open(licenseFile, "r")
    final_data = f.read()
    final_data = final_data.replace("\n", "\r\n")
    resp = HttpResponse(final_data, content_type="text/plain")
    resp['Content-Disposition'] = 'attachment; filename="licenseserver.lic"'
    return resp

@csrf_exempt
def generate_single_license(request):
    """ Add single license to database """

    #Create a master license object
    ml = MasterLicense()

    #Set master license fields
    ml.m_licenseType = "Single License"
    ml.m_organizationName = request.POST.get('orgname', '')
    ml.m_emailAddress = request.POST.get('email', '')
    ml.m_phoneNumber = request.POST.get('phone', '')
    #ml.m_notes = request.POST.get('notes', '')  
    ml.save()


    #Get product license fields
    organizationName = request.POST.get('orgname', '')

    grades = request.POST.get('grade', '')
    grade_arr = grades.split(';')
    grade_arr.pop()
    
    start_dates = request.POST.get('sd', '')
    start_date_arr = start_dates.split(';')
    start_date_arr.pop()
    
    end_dates = request.POST.get('ed', '')
    end_date_arr = end_dates.split(';')
    end_date_arr.pop()
    
    exp_dates = request.POST.get('exd', '')
    exp_date_arr = exp_dates.split(';')
    exp_date_arr.pop()

    support_ids = request.POST.get('sid', '')
    support_id_arr = support_ids.split(';')
    support_id_arr.pop()
    
    license_types = request.POST.get('perm', '')
    license_type_arr = license_types.split(';')
    license_type_arr.pop()
    
    number_ips = request.POST.get('ips', '')
    number_ips_arr = number_ips.split(';')
    number_ips_arr.pop()
    
    hostips_allowed = request.POST.get('hip', '')
    hostip_allowed_arr = hostips_allowed.split(';')
    hostip_allowed_arr.pop()
    
    logs = request.POST.get('log', '')
    log_arr = logs.split(';')
    log_arr.pop()
    
    tasks = request.POST.get('task', '')
    task_arr = tasks.split(';')
    task_arr.pop()
    
    nodes = request.POST.get('node', '')
    node_arr = nodes.split(';')
    node_arr.pop()
    
    systems = request.POST.get('sys', '')
    system_arr = systems.split(';')
    system_arr.pop()
    
    snmps = request.POST.get('snmp', '')
    snmp_arr = snmps.split(';')
    snmp_arr.pop()
    
    names = request.POST.get('name', '')
    product_name_arr = names.split(';')
    product_name_arr.pop()
    
    versions = request.POST.get('vers', '')
    product_vers_arr = versions.split(';')
    product_vers_arr.pop()
    
    num_stations = request.POST.get('station', '')
    num_stations_arr = num_stations.split(';')
    num_stations_arr.pop()
    pl = ProductLicense()

    for i in range (0, len(num_stations_arr)):

        #Create a product license object

        #Add master license to product license
        pl.masterLicense = ml

        #Set host ip info
        tmp_product_allowed_host_ip = hostip_allowed_arr[0]
        pl.m_host_IP = tmp_product_allowed_host_ip.strip()
        ml.m_IP_Host =  hostip_allowed_arr[0] 


        pl.m_stations = int(num_stations_arr[0])
        pl.m_ips = int(number_ips_arr[0])
        pl.m_task = int(task_arr[0])
        pl.m_log = int(log_arr[0])
        pl.m_node = int(node_arr[0])
        pl.m_sys = int(system_arr[0])
        pl.m_snmp = int(snmp_arr[0])
        pl.m_supportID = support_id_arr[0]
        pl.m_expirationDate = round(calendar.timegm(datetime.datetime.strptime(exp_date_arr[0], "%Y-%m-%d %H:%M:%S").timetuple()))
        pl.m_productName = product_name_arr[0]
        pl.m_productVersion = product_vers_arr[0]
        pl.m_grade = grade_arr[0]
        pl.m_lineNumber = 0
        if (license_type_arr[0]=="true"):
            pl.m_permanent = 1
            pl.m_startDate = 0
            pl.m_endDate = 0
        else:
            pl.m_permanent = 0
            pl.m_startDate = round(calendar.timegm(datetime.datetime.strptime(start_date_arr[0], "%Y-%m-%d %H:%M:%S").timetuple()))
            pl.m_endDate = round(calendar.timegm(datetime.datetime.strptime(end_date_arr[0], "%Y-%m-%d %H:%M:%S").timetuple()))

        if (hostip_allowed_arr[0] == "token") or (hostip_allowed_arr[0] == "token24"):
            pl.m_licType = hostip_allowed_arr[0]
        else:
            pl.m_licType = "normal"
    
        pl.save()

    cleartextheader = pl.get_product_clear_text_line_s()
    # codedKeysText = "Key=" + pl.get_product_key(organizationName)
    codedKeysText = "Key=" + "MyTempKey"

    
    cleartextheader = cleartextheader + "\n" + codedKeysText
    ml.m_textFile = cleartextheader
    ml.m_user = request.user.get_username()
    ml.save()
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    outputFile = BASE_DIR + "/bin/-product-License.lic"
    f = open(outputFile, "w")
    f.write(cleartextheader)
    final_data = {}
    final_data['success'] = True
    logging.info("User: " + str(request.user.username) + 
                 " has created Single License #: " + str(ml.id))
    return HttpResponse(json.dumps(final_data), content_type="application/json")

def download_single_license_file(request, productName = "AppLoader", productVersion = ""):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    licenseFile = BASE_DIR + "/bin/-product-License.lic"
    f = open(licenseFile, "r")
    final_data = f.read()
    f_name = productName + "License.lic"
    if (productName.lower() == "scenariobuilder"):
        f_name = "sblicense.lic"
    elif(productName.lower() == "scenariostation" and newScenarioStationLicenseName(productVersion)):
        f_name = "sslicense.lic"
    elif(productName.lower() == "scenariostation"):
        f_name = "awlicense.lic"
    elif(productName.lower() == "rtester"):
        f_name = "rtester.lic"
    elif(productName.lower() == "rworker"):
        f_name = "rworker.lic"
    elif(productName.lower() == "rft"):
        f_name = "empty.lic"
        final_data = ""
    elif(productName.lower() == "rpa"):
        f_name = "empty.lic"
        final_data = ""
    final_data = final_data.replace("\n", "\r\n")
    resp = HttpResponse(final_data, content_type="text/plain")
    resp['Content-Disposition'] = 'attachment; filename="' + f_name + '"'
    return resp
    
def newScenarioStationLicenseName(ScenarioStationVersion = ""):
    newFileName = False
    try:
        ver = float(ScenarioStationVersion)
        if (ver > 8.1):
            newFileName = True
    except:
        newFileName = False
    return newFileName