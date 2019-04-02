from django.shortcuts import render, redirect
from django.contrib.auth.signals import user_logged_out
from django.contrib import messages
from .cashlogform import CashentryForm, EmployeeForm, LocationsForm, PatientPayForm, CashentryUpdateForm, EmployeeUpdateForm, LocationsUpdateForm, PatientPayUpdateForm
from .auditform import AuditForm
from .models import Cashentry, Employee, Locations, Patientpay, Audit
from django.contrib.auth.hashers import check_password
import datetime


def logoutUser(sender, request, **kwargs):
    messages.SUCCESS(request, 'You have been logged out!')


# basline form page


def cform(request):
    user_logged_out.connect(logoutUser)

    cashForm = CashentryForm()
    employFormc = EmployeeForm(prefix='cashlog')
    employFormp = EmployeeForm(prefix='ptpay')
    locFormc = LocationsForm(prefix='cashlog')
    locFormp = LocationsForm(prefix='ptpay')
    ptPayForm = PatientPayForm()

    context = {
        'cashForm': cashForm,
        'employFormc': employFormc,
        'employFormp': employFormp,
        'locFormc': locFormc,
        'locFormp': locFormp,
        'ptPayForm': ptPayForm,
    }

    return render(request, 'mainforms/cashlog.html', context)

# usage -this function below will be reused in any views that require post values from cashform
# purpose-  takes the post cashform values and prepares them for insertion
# to database


def cashArrayPost(postrequest):
    cashDict = {}
    cashArray = ['onec', 'fivec', 'tenc', 'twfvc', 'oned', 'twod',
                 'fived', 'tend', 'twntd', 'recount', 'entrydate', 'shifttime']
    pureCash = cashArray[:9]
    for item in cashArray:
        cashDict[item] = postrequest.get(item)

    if (cashDict['recount'] == '') or (cashDict['recount'] is None):
        cashDict['recount'] = 'No'
    else:
        cashDict['recount'] = 'Yes'
    cashDict['entrydate'] = datetime.datetime.strptime(
        cashDict['entrydate'], '%m/%d/%Y')

    for key in pureCash:
        if (cashDict[key] == '') or (cashDict[key] is None):
            cashDict[key] = 0
        else:
            cashDict[key] = float(cashDict[key])
    return cashDict

# usage - this function below can be reused for any patientpay view
# requiring post values from ptpay form


def patientPayPost(postrequest):
    ptpayDict = {}
    ptpayArray = ['datepay', 'ptnamepay', 'ptidpay', 'otherpay',
                  'amountpay', 'payitem', 'payitem', 'paytype']
    for item in ptpayArray:
        ptpayDict[item] = postrequest.get(item)

    ptpayDict['datepay'] = datetime.datetime.strptime(
        ptpayDict['datepay'], '%m/%d/%Y')
    return ptpayDict


# this view below deals with cashlog form submit request
def clogFormView(request):
    cashForm = CashentryForm(request.POST)
    employFormc = EmployeeForm(request.POST, prefix='cashlog')
    locFormc = LocationsForm(request.POST, prefix='cashlog')
    cashformerrors = CashentryForm(request.POST).errors

    if cashForm.is_valid() and employFormc.is_valid() and locFormc.is_valid():
        clogname = request.POST.get('cashlog-staffname')
        cloglocation = request.POST.get('cashlog-locname')
        postCashArray = cashArrayPost(request.POST)

        checkEmployee = Employee.objects.filter(staffname=clogname)
        getLocation = Locations.objects.get(locname=cloglocation)
        clogTotalcash = (postCashArray['onec'] * .01) + (postCashArray['fivec'] * .05) + (postCashArray['tenc'] * .1) + (postCashArray['twfvc'] * .25) + (
            postCashArray['oned'] * 1) + (postCashArray['twod'] * 2) + (postCashArray['fived'] * 5) + (postCashArray['tend'] * 10) + (postCashArray['twntd'] * 20)
        clogRoundedTotalCash = round(clogTotalcash, 2)

        if checkEmployee:
            getEmployee = Employee.objects.get(staffname=clogname)
            Cashentry.objects.create(onec=postCashArray['onec'], fivec=postCashArray['fivec'], tenc=postCashArray['tenc'], twfvc=postCashArray['twfvc'], oned=postCashArray['oned'], twod=postCashArray['twod'], fived=postCashArray['fived'], tend=postCashArray['tend'], twntd=postCashArray['twntd'], staffid=getEmployee.staffid, locid=getLocation.locid, shifttime=postCashArray['shifttime'], entrydate=postCashArray['entrydate'],
                                     totalcash=clogRoundedTotalCash, recount=postCashArray['recount'])
        else:
            Employee.objects.create(staffname=clogname)
            getEmployee = Employee.objects.get(staffname=clogname)
            Cashentry.objects.create(onec=postCashArray['onec'], fivec=postCashArray['fivec'], tenc=postCashArray['tenc'], twfvc=postCashArray['twfvc'], oned=postCashArray['oned'], twod=postCashArray['twod'], fived=postCashArray['fived'], tend=postCashArray['tend'], twntd=postCashArray['twntd'], staffid=getEmployee.staffid, locid=getLocation.locid, shifttime=postCashArray['shifttime'], entrydate=postCashArray['entrydate'],
                                     totalcash=clogRoundedTotalCash, recount=postCashArray['recount'])

        return render(request, 'mainforms/test.html', {'test2': cashformerrors})
    else:
        return render(request, 'mainforms/test.html', {'test2': cashformerrors})

# this view below deals with patient pay form submit request


def ptpayFormView(request):
    ptPayForm = PatientPayForm(request.POST)
    employFormp = EmployeeForm(request.POST, prefix='ptpay')
    locFormp = LocationsForm(request.POST, prefix='ptpay')
    locformerrors = LocationsForm(prefix='ptpay').errors

    if ptPayForm.is_valid() and employFormp.is_valid() and locFormp.is_valid():
        ptpayName = request.POST.get('ptpay-staffname')
        ptpayLocation = request.POST.get('ptpay-locname')
        ptpayPatientName = request.POST.get('ptnamepay')
        ptpayPaitentID = request.POST.get('ptidpay')
        ptpayPayItem = request.POST.get('payitem')
        ptpayPayType = request.POST.get('paytype')
        ptpayBreakdown = request.POST.get('otherpay')
        ptpayAmount = request.POST.get('amountpay')
        ptpayEntryDate = request.POST.get('datepay')

        checkEmployee = Employee.objects.filter(staffname=ptpayName)
        getLocation = Locations.objects.get(locname=ptpayLocation)
        ptpayConvertedDate = datetime.datetime.strptime(
            ptpayEntryDate, '%m/%d/%Y')

        if checkEmployee:
            getEmployee = Employee.objects.get(staffname=ptpayName)
            Patientpay.objects.create(datepay=ptpayConvertedDate, ptnamepay=ptpayPatientName, ptidpay=ptpayPaitentID, otherpay=ptpayBreakdown,
                                      amountpay=ptpayAmount, staffid=getEmployee.staffid, locid=getLocation.locid, payitem=ptpayPayItem, paytype=ptpayPayType)
        else:
            Employee.objects.create(staffname=ptpayName)
            getEmployee = Employee.objects.get(staffname=ptpayName)
            Patientpay.objects.create(datepay=ptpayConvertedDate, ptnamepay=ptpayPatientName, ptidpay=ptpayPaitentID, otherpay=ptpayBreakdown,
                                      amountpay=ptpayAmount, staffid=getEmployee.staffid, locid=getLocation.locid, payitem=ptpayPayItem, paytype=ptpayPayType)

    return render(request, 'mainforms/test.html', {'test': locformerrors})

# this view displays report results and filters location if a location is
# picked


def resultViewClog(request, parameter='none'):
    if parameter == 'none':
        last_hundred_msges = Cashentry.objects.all(
        ).order_by('-entrydate')[:100]
        for item in last_hundred_msges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/reportclog.html', {'cashreport': last_hundred_msges})
    else:
        getLoc = Locations.objects.get(locname=parameter)
        getLocId = getLoc.locid
        last_hundred_msges = Cashentry.objects.filter(
            locid=getLocId).order_by('-entrydate')[:100]
        for item in last_hundred_msges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/reportclog.html', {'cashreport': last_hundred_msges})


def resultViewPtpay(request, parameter='none'):
    if parameter == 'none':
        last_hundred_ptpaymsges = Patientpay.objects.all(
        ).order_by('-datepay')[:100]
        for item in last_hundred_ptpaymsges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/reportptpay.html', {'ptpayreport': last_hundred_ptpaymsges})
    else:
        getLoc = Locations.objects.get(locname=parameter)
        getLocId = getLoc.locid
        last_hundred_ptpaymsges = Patientpay.objects.filter(
            locid=getLocId).order_by('-datepay')[:100]
        for item in last_hundred_ptpaymsges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/reportptpay.html', {'ptpayreport': last_hundred_ptpaymsges})

# this view is por ptpay report edit page or itemedit page depending on
# parameter


def resultViewPtpayEdit(request, parameter='none'):
    if parameter == 'none':
        last_hundred_ptpaymsges = Patientpay.objects.all(
        ).order_by('-datepay')[:100]
        for item in last_hundred_ptpaymsges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/reportptpayedit.html', {'ptpayreport': last_hundred_ptpaymsges})
    else:
        editEntry = Patientpay.objects.get(entryidp=parameter)
        convertedDate = datetime.datetime.strptime(
            str(editEntry.datepay), '%Y-%m-%d').strftime('%m/%d/%Y')
        editForm = PatientPayUpdateForm(instance=editEntry)
        getEmp = Employee.objects.get(staffid=editEntry.staffid)
        editEmp = EmployeeUpdateForm(instance=getEmp)
        getLoc = Locations.objects.get(locid=editEntry.locid)
        editLoc = LocationsUpdateForm(instance=getLoc)
        return render(request, 'mainforms/ptpayitemedit.html', {'itemid': parameter, 'form': editForm, 'formdate': convertedDate, 'location': editLoc, 'staff': editEmp})

# this view displays last hundred entries but with edit button, if edit is
# clicked it takes you to the item edit mode


def reporteditView(request, parameter='none'):
    if parameter == 'none':
        last_hundred_msges = Cashentry.objects.all(
        ).order_by('-entrydate')[:100]
        for item in last_hundred_msges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/reportedit.html', {'report': last_hundred_msges})
    else:
        editEntry = Cashentry.objects.get(entryid=parameter)
        convertedDate = datetime.datetime.strptime(
            str(editEntry.entrydate), '%Y-%m-%d').strftime('%m/%d/%Y')
        editForm = CashentryUpdateForm(instance=editEntry)
        getEmp = Employee.objects.get(staffid=editEntry.staffid)
        editEmp = EmployeeUpdateForm(instance=getEmp)
        getLoc = Locations.objects.get(locid=editEntry.locid)
        editLoc = LocationsUpdateForm(instance=getLoc)
        return render(request, 'mainforms/reportitemedit.html', {'itemid': parameter, 'form': editForm, 'formdate': convertedDate, 'location': editLoc, 'staff': editEmp})

# this view below deals with cashentry item update request


def clogitemupdateView(request, parameter):
    cashFormUpdate = CashentryUpdateForm(request.POST)
    employFormUpdate = EmployeeUpdateForm(request.POST)
    locFormcUpdate = LocationsUpdateForm(request.POST)
    errorsCform = CashentryUpdateForm(request.POST).errors
    errorsEform = EmployeeUpdateForm(request.POST).errors
    errorsLform = LocationsUpdateForm(request.POST).errors

    staffname = request.POST.get('staffname')
    cloglocation = request.POST.get('locname')
    clogShifttime = request.POST.get('shifttime')
    recountValue = request.POST.get('recount')
    updateEntry = Cashentry.objects.filter(entryid=parameter)
    checkEmployee = Employee.objects.filter(staffname=staffname)
    getLocation = Locations.objects.get(locname=cloglocation)
    if checkEmployee:
        getEmployee = Employee.objects.get(staffname=staffname)
    else:
        Employee.objects.create(staffname=staffname)
        getEmployee = Employee.objects.get(staffname=staffname)

    auditEmpName = Employee.objects.get(
        staffid=updateEntry[0].staffid).staffname
    auditLocName = Locations.objects.get(locid=updateEntry[0].locid).locname
    formType = 'cashlog'
    username = request.user

    auditMessage = f'Modified cash log entry with following values: Date:{updateEntry[0].entrydate} Staffname:{auditEmpName} location: {auditLocName} \
            $.01:{updateEntry[0].onec} $.05:{updateEntry[0].fivec} $.1:{updateEntry[0].tenc} $.25:{updateEntry[0].twfvc} $1:{updateEntry[0].oned} $5:{updateEntry[0].fived} $10:{updateEntry[0].tend} $20:{updateEntry[0].twntd} Total Cash: {updateEntry[0].totalcash} Recount: {updateEntry[0].recount}'
    Audit.objects.create(superuser=username, modifiedentry=auditMessage,
                         modifiedentryid=updateEntry[0].entryid, audittype=formType)

    # this function takes the request.post array and sets all null cash values
    # to 0 or converts it to float
    postCashArray = cashArrayPost(request.POST)

    clogTotalcash = (postCashArray['onec'] * .01) + (postCashArray['fivec'] * .05) + (postCashArray['tenc'] * .1) + (postCashArray['twfvc'] * .25) + (
        postCashArray['oned'] * 1) + (postCashArray['twod'] * 2) + (postCashArray['fived'] * 5) + (postCashArray['tend'] * 10) + (postCashArray['twntd'] * 20)
    clogRoundedTotalCash = round(clogTotalcash, 2)
    updateEntry.update(onec=postCashArray['onec'], fivec=postCashArray['fivec'], tenc=postCashArray['tenc'], twfvc=postCashArray['twfvc'], oned=postCashArray['oned'], twod=postCashArray['twod'], fived=postCashArray['fived'], tend=postCashArray['tend'], twntd=postCashArray['twntd'], staffid=getEmployee.staffid, locid=getLocation.locid, shifttime=postCashArray['shifttime'],
                       entrydate=postCashArray['entrydate'], totalcash=clogRoundedTotalCash, recount=postCashArray['recount'])
    return render(request, 'mainforms/test.html', {'test': errorsCform})


def ptpayItemEditView(request, parameter):
    ptpayFormUpdate = PatientPayUpdateForm(request.POST)
    employFormUpdate = EmployeeUpdateForm(request.POST)
    locFormcUpdate = LocationsUpdateForm(request.POST)

    postPtpayArray = patientPayPost(request.POST)
    staffname = request.POST.get('staffname')
    ptpayLocation = request.POST.get('locname')
    ptpayConvertedDate = request.POST.get(
        'datepay')  # this conversion happens in form
    updateEntry = Patientpay.objects.filter(
        entryidp=parameter)  # used for updating entry
    auditEmpName = Employee.objects.get(
        staffid=updateEntry[0].staffid).staffname
    auditLocName = Locations.objects.get(locid=updateEntry[0].locid).locname
    checkEmployee = Employee.objects.filter(staffname=staffname)
    getLocation = Locations.objects.get(locname=ptpayLocation)
    username = request.user

    if checkEmployee:
        getEmployee = Employee.objects.get(staffname=staffname)
    else:
        Employee.objects.create(staffname=staffname)
        getEmployee = Employee.objects.get(staffname=staffname)

    auditMessage = f'Modified patient pay entry, previous values were: Date:{updateEntry[0].datepay} Staffname:{auditEmpName} location:{auditLocName} \
            Patient Name: {updateEntry[0].ptnamepay} Patient ID: {updateEntry[0].ptidpay}  Payment Item: {updateEntry[0].payitem} Payment Type: {updateEntry[0].paytype} Amount: {updateEntry[0].amountpay}  comment: {updateEntry[0].otherpay}'
    Audit.objects.create(superuser=username, modifiedentry=auditMessage,
                         modifiedentryid=updateEntry[0].entryidp, audittype='patientpay')

    updateEntry.update(datepay=postPtpayArray['datepay'], ptnamepay=postPtpayArray['ptnamepay'], ptidpay=postPtpayArray['ptidpay'], otherpay=postPtpayArray[
                       'otherpay'], amountpay=postPtpayArray['amountpay'], staffid=getEmployee.staffid, locid=getLocation.locid, payitem=postPtpayArray['payitem'], paytype=postPtpayArray['paytype'])
    return render(request, 'mainforms/test.html')


def superUserview(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    messages.success(request, f'Hello {username} , please select a report below to edit:')
    return render(request, 'mainforms/superuser.html')


def deleteView(request):
    successMessage = 'Item is now deleted'
    notSuccessMessage = 'Password Incorrect'
    if request.user.is_authenticated:
        username = request.user
        rawpass = request.POST.get('password')

        if check_password(rawpass, request.user.password):
            ptpayEntryId = request.POST.get('deletedID')
            ptPayObject = Patientpay.objects.get(
                entryidp=ptpayEntryId)  # object to be deleted
            ptpayStaffID = ptPayObject.staffid
            ptpayLocID = ptPayObject.locid
            employeeName = Employee.objects.get(staffid=ptpayStaffID).staffname
            locationName = Locations.objects.get(locid=ptpayLocID).locname
            ptpaydate = ptPayObject.datepay
            patientname = ptPayObject.ptnamepay
            patientid = ptPayObject.ptidpay
            comments = ptPayObject.otherpay
            ptpayitem = ptPayObject.payitem
            ptpayType = ptPayObject.paytype
            ptpayAmount = ptPayObject.amountpay
            formType = 'patientpay'

            auditMessage = f'deleted patient pay entry with the following values: Date:{ptpaydate} Staffname:{employeeName} location:{locationName} \
            Patient Name: {patientname} Patient ID: {patientid}  Payment Item: {ptpayitem} Payment Type: {ptpayType} Amount: {ptpayAmount}  comment: {comments}'
            Audit.objects.create(superuser=username, modifiedentry=auditMessage,
                                 modifiedentryid=ptpayEntryId, audittype=formType)
            ptPayObject.delete()

            return render(request, 'mainforms/deleteItem.html', {'passMessage': successMessage, 'test': auditMessage})

        else:
            return render(request, 'mainforms/deleteItem.html', {'passMessage': notSuccessMessage})
    else:
        return render(request, 'mainforms/deleteItem.html', {'passMessage': notSuccessMessage})


def deleteViewCashlog(request):
    successMessage = 'Item is now deleted'
    notSuccessMessage = 'Password Incorrect'
    if request.user.is_authenticated:
        username = request.user
        rawpass = request.POST.get('password')

        if check_password(rawpass, request.user.password):
            cashlogEntryId = request.POST.get('deletedID')
            cashentryObject = Cashentry.objects.get(entryid=cashlogEntryId)
            onecVal = cashentryObject.onec
            fivecVal = cashentryObject.fivec
            tencVal = cashentryObject.tenc
            twfvcVal = cashentryObject.twfvc
            onedVal = cashentryObject.oned
            twodVal = cashentryObject.twod
            fivedVal = cashentryObject.fived
            tendVal = cashentryObject.tend
            twntdVal = cashentryObject.twntd
            entrydateVal = cashentryObject.entrydate
            totalcashVal = cashentryObject.totalcash
            recountVal = cashentryObject.recount
            formType = 'cashlog'

            cashentryStaffID = cashentryObject.staffid
            cashentryLocID = cashentryObject.locid
            employeeName = Employee.objects.get(
                staffid=cashentryStaffID).staffname
            locationName = Locations.objects.get(locid=cashentryLocID).locname

            auditMessage = f'deleted cash log entry with following values: Date:{entrydateVal} Staffname:{employeeName} location: {locationName} \
            $.01:{onecVal} $.05:{fivecVal} $.1:{tencVal} $.25:{twfvcVal} $1:{onedVal} $5:{fivedVal} $10:{tendVal} $20:{twntdVal} Total Cash: {totalcashVal} Recount: {recountVal}'
            Audit.objects.create(superuser=username, modifiedentry=auditMessage,
                                 modifiedentryid=cashlogEntryId, audittype=formType)
            cashentryObject.delete()

            return render(request, 'mainforms/deleteItem.html', {'passMessage': auditMessage})


def auditView(request):
    auditForm = AuditForm()
    return render(request, 'mainforms/audit.html', {'auditForm': auditForm})
    # elif parameter == 'patientpay':
 #   results = Audit.objects.filter(
  #      audittype='patientpay').order_by('-deletedate')
   # return render(request, 'mainforms/audit-ptpay.html', {'results': results})
    # elif parameter == 'cashlog':
 #   results = Audit.objects.filter(
  #      audittype='patientpay').order_by('-deletedate')
   # return render(request, 'mainforms/audit-cashlog.html', {'results':
   # results})


def auditViewPost(request):
    auditform = AuditForm(request.POST)
    if AuditForm().is_valid:
        startdate = request.POST.get('start_date')
        enddate = request.POST.get('end_date')
        audittype = request.POST.get('audit_type')
        formatStartDate = datetime.datetime.strptime(
            startdate, "%m/%d/%Y").strftime("%Y-%m-%d")
        formatEndDate = datetime.datetime.strptime(
            enddate, "%m/%d/%Y").strftime("%Y-%m-%d")

        filteredResults = Audit.objects.filter(audittype=audittype,
                                               modifieddate__range=[formatStartDate, formatEndDate])
        return render(request, 'mainforms/audit-ptpay.html', {'data': filteredResults})
    else:
        return render(request, 'mainforms/audit-ptpay.html', {'data': audittype})
