# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-16 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0004_collection_collectionlabel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Google_Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_resource_name', models.CharField(max_length=50)),
                ('contact_name', models.CharField(max_length=200)),
                ('contact_email', models.CharField(default='', max_length=200)),
                ('contact_phone_no', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
