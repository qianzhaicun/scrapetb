# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_auto_20171106_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyingitem',
            name='no',
            field=models.IntegerField(null=True, verbose_name='NO'),
        ),
    ]
