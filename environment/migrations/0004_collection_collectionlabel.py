# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-16 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0003_document_documentfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='collectionLabel',
            field=models.CharField(default='No Label', max_length=50),
        ),
    ]
