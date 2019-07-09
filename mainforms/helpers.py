import datetime


# helper functions


# usage -this function cashArrayPost below will be reused in any views that require post values from cashform
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


# usage - this function patientPayPost below will be reused in any views that require post values from patient pay form
# this takes the post values and prepares them for insertion into database.
def patientPayPost(postrequest):
    ptpayDict = {}
    ptpayArray = ['datepay', 'ptnamepay', 'ptidpay', 'otherpay',
                  'amountpay', 'payitem', 'payitem', 'paytype']
    for item in ptpayArray:
        ptpayDict[item] = postrequest.get(item)

    ptpayDict['datepay'] = datetime.datetime.strptime(
        ptpayDict['datepay'], '%m/%d/%Y')
    return ptpayDict
