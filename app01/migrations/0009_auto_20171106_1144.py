# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_auto_20171106_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyingitem',
            name='buying_url',
            field=models.URLField(verbose_name='采购地址', max_length=500),
        ),
    ]
