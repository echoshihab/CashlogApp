# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from django.db import models
from django.core.validators import MaxValueValidator


class Cashentry(models.Model):
    # Field name made lowercase.
    entryid = models.AutoField(db_column='EntryID', primary_key=True)
    onec = models.IntegerField(MaxValueValidator(999), blank=True)
    fivec = models.IntegerField(MaxValueValidator(999), blank=True)
    tenc = models.IntegerField(MaxValueValidator(999), blank=True)
    twfvc = models.IntegerField(MaxValueValidator(999), blank=True)
    oned = models.IntegerField(MaxValueValidator(999), blank=True)
    twod = models.IntegerField(MaxValueValidator(999), blank=True)
    fived = models.IntegerField(MaxValueValidator(999), blank=True)
    tend = models.IntegerField(MaxValueValidator(999), blank=True)
    twntd = models.IntegerField(MaxValueValidator(999), blank=True)
    # Field name made lowercase.
    staffid = models.IntegerField(db_column='StaffID')
    # Field name made lowercase.
    locid = models.IntegerField(db_column='LocID')
    # Field name made lowercase.
    shifttime = models.CharField(db_column='ShiftTime', max_length=40)
    # Field name made lowercase.
    entrydate = models.DateField(db_column='EntryDate')
    totalcash = models.FloatField()
    # Field name made lowercase.
    recount = models.CharField(db_column='Recount', max_length=40)

    class Meta:
        managed = False
        db_table = 'cashentry'


class Employee(models.Model):
    # Field name made lowercase.
    staffid = models.AutoField(db_column='StaffID', primary_key=True)
    # Field name made lowercase.
    staffname = models.CharField(db_column='StaffName', max_length=20)

    class Meta:
        managed = False
        db_table = 'employee'


class Locations(models.Model):
    # Field name made lowercase.
    locid = models.AutoField(db_column='LocID', primary_key=True)
    # Field name made lowercase.
    locname = models.CharField(db_column='LocName', max_length=255)

    class Meta:
        managed = False
        db_table = 'locations'


class Patientpay(models.Model):
    datepay = models.DateField()
    ptnamepay = models.CharField(max_length=40, blank=True, null=True)
    ptidpay = models.CharField(max_length=20, blank=True, null=True)
    otherpay = models.CharField(max_length=40, blank=True, null=True)
    amountpay = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True)
    # Field name made lowercase.
    staffid = models.IntegerField(db_column='StaffID', blank=True, null=True)
    # Field name made lowercase.
    locid = models.IntegerField(db_column='LocID')
    # Field name made lowercase.
    entryidp = models.AutoField(db_column='EntryIDp', primary_key=True)
    payitem = models.CharField(max_length=40, blank=True, null=True)
    paytype = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patientpay'

# this audit below is for patient pay form


class Audit(models.Model):
    entryid = models.AutoField(primary_key=True)
    # for holding superuser name
    superuser = models.CharField(default='admin', max_length=200)
    # for holding date of deletion
    modifieddate = models.DateField(auto_now=True, null=True)
    modifiedentryid = models.IntegerField(
        null=True)  # for the id# of item deleted
    audittype = models.CharField(
        default='none', max_length=100)  # cashlog vs patientpay
    modifiedentry = models.CharField(max_length=200)
