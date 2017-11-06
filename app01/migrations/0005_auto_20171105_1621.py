# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20171105_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyingitem',
            name='clearance_sign_id',
            field=models.ForeignKey(null=True, verbose_name='通关符号', to='app01.Transport_way', related_name='clearance_sign_id'),
        ),
        migrations.AlterField(
            model_name='buyingitem',
            name='transport_company_id',
            field=models.ForeignKey(null=True, verbose_name='运输公司', to='app01.Transport_way', related_name='transport_company_id'),
        ),
        migrations.AlterField(
            model_name='buyingitem',
            name='transport_way_id',
            field=models.ForeignKey(null=True, verbose_name='货运方式', to='app01.Transport_way', related_name='transport_way_id'),
        ),
    ]
