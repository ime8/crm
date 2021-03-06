# Generated by Django 2.2.3 on 2019-09-11 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_userprofile_stu_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='stu_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='所关联的客户'),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('summary', models.CharField(max_length=32, verbose_name='简介')),
                ('img', models.ImageField(upload_to='./statics/img/Video/', verbose_name='图片')),
                ('href', models.CharField(max_length=256, verbose_name='视频地址')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Category')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Level')),
            ],
        ),
    ]
