# Generated by Django 2.1.2 on 2019-04-02 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainforms', '0004_auto_20190402_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audit',
            old_name='deletedate',
            new_name='modifieddate',
        ),
    ]