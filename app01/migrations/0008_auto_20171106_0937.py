# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_buyingitem_chinese_kind_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyingitem',
            name='clearance_sign_id',
            field=models.ForeignKey(null=True, related_name='clearance_sign_id', to='app01.Clearance_sign', verbose_name='通关符号'),
        ),
    ]
