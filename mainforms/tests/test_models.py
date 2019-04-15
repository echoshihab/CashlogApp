import datetime
from django.test import TestCase
from django.urls import reverse

from mainforms.models import Cashentry, Employee, Locations, Patientpay, Audit
from decimal import Decimal


class CashentryTests(TestCase):

    def setUp(self):
        Cashentry.objects.create(onec=1, fivec=4, tenc=12, twfvc=11, oned=33, twod=44, fived=44, tend=11, twntd=20, staffid=2, locid=1, shifttime='start of shift',
                                 entrydate='2019-11-11', totalcash=1000, recount='yes')

    def test_entries(self):
        newEntry = Cashentry.objects.get(entryid=1)
        self.assertEquals(newEntry.onec, 1)
        self.assertEquals(newEntry.fivec, 4)
        self.assertEquals(newEntry.tenc, 12)
        self.assertEquals(newEntry.twfvc, 11)
        self.assertEquals(newEntry.oned, 33)
        self.assertEquals(newEntry.twod, 44)
        self.assertEquals(newEntry.fived, 44)
        self.assertEquals(newEntry.tend, 11)
        self.assertEquals(newEntry.twntd, 20)
        self.assertEquals(newEntry.staffid, 2)
        self.assertEquals(newEntry.locid, 1)
        self.assertEquals(newEntry.shifttime, 'start of shift')
        self.assertEquals(newEntry.entrydate, datetime.date(2019, 11, 11))
        self.assertEquals(newEntry.totalcash, 1000)
        self.assertEquals(newEntry.recount, 'yes')


class EmployeeTests(TestCase):

    def setUp(self):
        Employee.objects.create(staffname='kroberts')
        Employee.objects.create(staffname='jmohring')

    def test_entries(self):
        entry1 = Employee.objects.get(staffid=1)
        entry2 = Employee.objects.get(staffid=2)
        self.assertEquals(entry1.staffname, 'kroberts')
        self.assertEquals(entry2.staffname, 'jmohring')


class LocationsTests(TestCase):

    def setUp(self):
        Locations.objects.create(locname='Boler')
        Locations.objects.create(locname='Bradley')

    def test_entries(self):
        entry1 = Locations.objects.get(locid=1)
        entry2 = Locations.objects.get(locid=2)
        self.assertEquals(entry1.locname, 'Boler')
        self.assertEquals(entry2.locname, 'Bradley')


class PatientpayTests(TestCase):

    def setUp(self):
        Patientpay.objects.create(datepay='2019-11-11', ptnamepay='John', ptidpay='M023423', otherpay='Comments', amountpay='140.30', staffid=1,
                                  locid=2, payitem='Report', paytype='Visa')

    def test_entries(self):
        entry = Patientpay.objects.get(entryidp=1)
        self.assertEquals(entry.datepay, datetime.date(2019, 11, 11))
        self.assertEquals(entry.ptnamepay, 'John')
        self.assertEquals(entry.ptidpay, 'M023423')
        self.assertEquals(entry.otherpay, 'Comments')
        self.assertEquals(entry.amountpay, Decimal('140.30'))
        self.assertEquals(entry.staffid, 1)
        self.assertEquals(entry.locid, 2)
        self.assertEquals(entry.payitem, 'Report')
        self.assertEquals(entry.paytype, 'Visa')


class AuditTests(TestCase):

    def setUp(self):
        Audit.objects.create(superuser='admin', modifiedentryid=142, audittype='Cashlog',
                             modifiedentry='deleted the following values 1,2,3')

    def test_entries(self):
        entry = Audit.objects.get(entryid=1)
        self.assertEquals(entry.superuser, 'admin')
        self.assertEquals(entry.modifiedentryid, 142)
        self.assertEquals(entry.audittype, 'Cashlog')
        self.assertEquals(entry.modifiedentry,
                          'deleted the following values 1,2,3')
