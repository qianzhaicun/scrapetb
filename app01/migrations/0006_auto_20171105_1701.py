# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20171105_1621'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transport_company',
        ),
        migrations.RemoveField(
            model_name='buyingitem',
            name='transport_company_id',
        ),
    ]
