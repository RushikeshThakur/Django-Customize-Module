# Generated by Django 3.0 on 2020-07-10 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_activationprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activationprofile',
            old_name='expired',
            new_name='exp',
        ),
    ]
