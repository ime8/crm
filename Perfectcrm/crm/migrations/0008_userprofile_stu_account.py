# Generated by Django 2.2.3 on 2019-09-08 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20190902_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stu_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer'),
        ),
    ]