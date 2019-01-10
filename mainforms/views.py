from django.shortcuts import render
from .cashlogform import CashentryForm, EmployeeForm, LocationsForm, PatientPayForm, CashentryUpdateForm, EmployeeUpdateForm, LocationsUpdateForm
from .models import Cashentry, Employee, Locations, Patientpay
import datetime


# basline form page


def cform(request):
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
        'ptPayForm': ptPayForm
    }

    return render(request, 'mainforms/cashlog.html', context)

# usage -this function below will be reused in any views that require post values from cashform
# purpose-  takes the post cashform values and prepares them for insertion to database
def cashArrayPost(postrequest):
    cashDict = {}
    cashArray = ['onec', 'fivec', 'tenc', 'twfvc', 'oned', 'twod', 'fived', 'tend', 'twntd', 'recount', 'entrydate', 'shifttime']
    pureCash = cashArray[:9]
    for item in cashArray:
        cashDict[item] = postrequest.get(item)

    if (cashDict['recount'] == '') or (cashDict['recount'] is None):
        cashDict['recount'] = 'No'
    else:
        cashDict['recount'] = 'Yes'
    cashDict['entrydate'] = datetime.datetime.strptime(cashDict['entrydate'], '%m/%d/%Y')

    for key in pureCash:
        if (cashDict[key] == '') or (cashDict[key] is None):
                cashDict[key] = 0
        else:
                cashDict[key] = float(cashDict[key])
    return cashDict


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
        clogTotalcash = (postCashArray['onec'] * .01) + (postCashArray['fivec'] * .05) + (postCashArray['tenc'] * .1) + (postCashArray['twfvc'] * .25) + (postCashArray['oned'] * 1) + (postCashArray['twod'] * 2) + (postCashArray['fived'] * 5) + (postCashArray['tend'] * 10) + (postCashArray['twntd'] * 20)
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
        ptpayConvertedDate = datetime.datetime.strptime(ptpayEntryDate, '%m/%d/%Y')

        if checkEmployee:
            getEmployee = Employee.objects.get(staffname=ptpayName)
            Patientpay.objects.create(datepay=ptpayConvertedDate, ptnamepay=ptpayPatientName, ptidpay=ptpayPaitentID, otherpay=ptpayBreakdown, amountpay=ptpayAmount, staffid=getEmployee.staffid, locid=getLocation.locid, payitem=ptpayPayItem, paytype=ptpayPayType)
        else:
            Employee.objects.create(staffname=ptpayName)
            getEmployee = Employee.objects.get(staffname=ptpayName)
            Patientpay.objects.create(datepay=ptpayConvertedDate, ptnamepay=ptpayPatientName, ptidpay=ptpayPaitentID, otherpay=ptpayBreakdown, amountpay=ptpayAmount, staffid=getEmployee.staffid, locid=getLocation.locid, payitem=ptpayPayItem, paytype=ptpayPayType)

    return render(request, 'mainforms/test.html', {'test': locformerrors})

# this view displays report results and filters location if a location is picked
def resultViewClog(request, parameter='none'):
    if parameter == 'none':
        last_hundred_msges = Cashentry.objects.all().order_by('-entrydate')[:100]
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
        last_hundred_msges = Cashentry.objects.filter(locid=getLocId).order_by('-entrydate')[:100]
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
        last_hundred_ptpaymsges = Patientpay.objects.all().order_by('-datepay')[:100]
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
        last_hundred_ptpaymsges = Patientpay.objects.filter(locid=getLocId).order_by('-datepay')[:100]
        for item in last_hundred_ptpaymsges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/reportptpay.html', {'ptpayreport': last_hundred_ptpaymsges})

# this view displays last hundred entries but with edit button, if edit is clicked it takes you to the item edit mode
def reporteditView(request, parameter='none'):
    if parameter == 'none':
        last_hundred_msges = Cashentry.objects.all().order_by('-entrydate')[:100]
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
        editForm = CashentryUpdateForm(instance=editEntry)
        getEmp = Employee.objects.get(staffid=editEntry.staffid)
        editEmp = EmployeeUpdateForm(instance=getEmp)
        getLoc = Locations.objects.get(locid=editEntry.locid)
        editLoc = LocationsUpdateForm(instance=getLoc)
        return render(request, 'mainforms/reportitemedit.html', {'itemid': parameter, 'form': editForm, 'location': editLoc, 'staff': editEmp})

# this view below deals with cashentry item update request
def clogitemupdateView(request, parameter):
    cashFormUpdate = CashentryUpdateForm(request.POST)
    employFormUpdate = EmployeeUpdateForm(request.POST)
    locFormcUpdate = LocationsUpdateForm(request.POST)
    errorsCform = CashentryForm(request.POST).errors
    errorsEform = EmployeeUpdateForm(request.POST).errors
    errorsLform = LocationsUpdateForm(request.POST).errors


    clogname = request.POST.get('staffname')
    cloglocation = request.POST.get('locname')
    clogConvertedDate = request.POST.get('entrydate')
    clogShifttime = request.POST.get('shifttime')
    recountValue  = request.POST.get('recount')
    updateEntry = Cashentry.objects.filter(entryid=parameter)
    getEmployee = Employee.objects.get(staffname=clogname)
    getLocation = Locations.objects.get(locname=cloglocation)

    postCashArray = cashArrayPost(request.POST)
# this takes the above post array and sets all null cash values to 0 or converts it to float
    clogTotalcash = (postCashArray['onec'] * .01) + (postCashArray['fivec'] * .05) + (postCashArray['tenc'] * .1) + (postCashArray['twfvc'] * .25) + (postCashArray['oned'] * 1) + (postCashArray['twod'] * 2) + (postCashArray['fived'] * 5) + (postCashArray['tend'] * 10) + (postCashArray['twntd'] * 20)
    clogRoundedTotalCash = round(clogTotalcash, 2)
    updateEntry.update(onec=postCashArray['onec'], fivec=postCashArray['fivec'], tenc=postCashArray['tenc'], twfvc=postCashArray['twfvc'], oned=postCashArray['oned'], twod=postCashArray['twod'], fived=postCashArray['fived'], tend=postCashArray['tend'], twntd=postCashArray['twntd'], staffid=getEmployee.staffid, locid=getLocation.locid, shifttime=postCashArray['shifttime'],
     entrydate=postCashArray['entrydate'], totalcash=clogRoundedTotalCash, recount=postCashArray['recount'])
    return render(request, 'mainforms/test.html', {'test': errorsCform})