# Generated by Django 2.1.2 on 2019-03-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainforms', '0002_audit'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='audittype',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='audit',
            name='deletedate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='deletedentryid',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='superuser',
            field=models.CharField(default='admin', max_length=200),
        ),
    ]
