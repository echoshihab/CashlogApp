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

# following arrays and functions will be reused in multiple views 
cashArray = ['onec', 'fivec', 'tenc', 'twfvc', 'oned', 'twod', 'fived', 'tend', 'twntd']

def cashArrayPost(array):
    cashDict = {}
    for item in array:
        cashDict[item] = request.POST.get(item)
    return cashDict
# this function above takes the cashArray values and assigns post values to it to create a dictionary

# this view below deals with cashlog form submit request
def clogFormView(request):
    cashForm = CashentryForm(request.POST)
    employFormc = EmployeeForm(request.POST, prefix='cashlog')
    locFormc = LocationsForm(request.POST, prefix='cashlog')
    cashformerrors = CashentryForm(request.POST).errors

    if cashForm.is_valid() and employFormc.is_valid() and locFormc.is_valid():
        clogname = request.POST.get('cashlog-staffname')
        cloglocation = request.POST.get('cashlog-locname')
        clogrecount = request.POST.get('recount')
        clogEntryDate = request.POST.get('entrydate')
        clogShifttime = request.POST.get('shifttime')

# this function below takes the cashArray values and assigns post values to it to create a dictionary
        postCashArray = cashArrayPost(cashArray)
# this takes the above post array and sets all null cash values to 0 or converts it to float
        for key, value in postCashArray.items():
            if (postCashArray[key] == '') or (postCashArray[key] is None):
                postCashArray[key] = 0
            else:
                postCashArray[key] = float(value)

        checkEmployee = Employee.objects.filter(staffname=clogname)
        getLocation = Locations.objects.get(locname=cloglocation)
        clogConvertedDate = datetime.datetime.strptime(clogEntryDate, '%m/%d/%Y')
        clogTotalcash = (postCashArray['onec'] * .01) + (postCashArray['fivec'] * .05) + (postCashArray['tenc'] * .1) + (postCashArray['twfvc'] * .25) + (postCashArray['oned'] * 1) + (postCashArray['twod'] * 2) + (postCashArray['fived'] * 5) + (postCashArray['tend'] * 10) + (postCashArray['twntd'] * 20)
        clogRoundedTotalCash = round(clogTotalcash, 2)

        if (clogrecount == '') or (clogrecount is None):
            recountValue = 'No'
        else:
            recountValue = 'Yes'

        if checkEmployee:
            getEmployee = Employee.objects.get(staffname=clogname)
            Cashentry.objects.create(onec=postCashArray['onec'], fivec=postCashArray['fivec'], tenc=postCashArray['tenc'], twfvc=postCashArray['twfvc'], oned=postCashArray['oned'], twod=postCashArray['twod'], fived=postCashArray['fived'], tend=postCashArray['tend'], twntd=postCashArray['twntd'], staffid=getEmployee.staffid, locid=getLocation.locid, shifttime=clogShifttime, entrydate=clogConvertedDate, totalcash=clogRoundedTotalCash, recount=recountValue)
        else:
            Employee.objects.create(staffname=clogname)
            getEmployee = Employee.objects.get(staffname=clogname)
            Cashentry.objects.create(onec=postCashArray['onec'], fivec=postCashArray['fivec'], tenc=postCashArray['tenc'], twfvc=postCashArray['twfvc'], oned=postCashArray['oned'], twod=postCashArray['twod'], fived=postCashArray['fived'], tend=postCashArray['tend'], twntd=postCashArray['twntd'], staffid=getEmployee.staffid, locid=getLocation.locid, shifttime=clogShifttime, entrydate=clogConvertedDate, totalcash=clogRoundedTotalCash, recount=recountValue)

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
def resultView(request, parameter='none'):
    if parameter == 'none':
        last_hundred_msges = Cashentry.objects.all().order_by('-entrydate')[:100]
        for item in last_hundred_msges:
            getEmp = Employee.objects.get(staffid=item.staffid)
            replace_id_w_name = getEmp.staffname
            item.staffid = replace_id_w_name
            getLoc = Locations.objects.get(locid=item.locid)
            replace_id_w_loc = getLoc.locname
            item.locid = replace_id_w_loc
        return render(request, 'mainforms/report.html', {'report': last_hundred_msges})
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
        return render(request, 'mainforms/report.html', {'report': last_hundred_msges})

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

    postCashArray = cashArrayPost(cashArray)
# this takes the above post array and sets all null cash values to 0 or converts it to float
    for key, value in postCashArray.items():
        if (postCashArray[key] == '') or (postCashArray[key] is None):
            postCashArray[key] = 0
        else:
            postCashArray[key] = float(value)

    clogTotalcash = (postCashArray['onec'] * .01) + (postCashArray['fivec'] * .05) + (postCashArray['tenc'] * .1) + (postCashArray['twfvc'] * .25) + (postCashArray['oned'] * 1) + (postCashArray['twod'] * 2) + (postCashArray['fived'] * 5) + (postCashArray['tend'] * 10) + (postCashArray['twntd'] * 20)
    clogRoundedTotalCash = round(clogTotalcash, 2)
    updateEntry.update(onec=postCashArray['onec'], fivec=postCashArray['fivec'], tenc=postCashArray['tenc'], twfvc=postCashArray['twfvc'], oned=postCashArray['oned'], twod=postCashArray['twod'], fived=postCashArray['fived'], tend=postCashArray['tend'], twntd=postCashArray['twntd'], staffid=getEmployee.staffid, locid=getLocation.locid, shifttime=clogShifttime, entrydate=clogConvertedDate, totalcash=clogRoundedTotalCash, recount=recountValue)
    return render(request, 'mainforms/test.html', {'test': errorsCform})