# Generated by Django 2.2.3 on 2019-09-02 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20190828_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='常用邮箱'),
        ),
        migrations.AddField(
            model_name='customer',
            name='id_num',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
