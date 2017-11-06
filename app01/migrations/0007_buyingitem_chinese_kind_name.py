# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20171105_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyingitem',
            name='chinese_kind_name',
            field=models.CharField(default=datetime.datetime(2017, 11, 5, 9, 24, 51, 94738, tzinfo=utc), max_length=200, verbose_name='中文品名'),
            preserve_default=False,
        ),
    ]
