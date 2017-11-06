# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20171105_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyingitem',
            name='add_express_fee',
            field=models.DecimalField(null=True, verbose_name='快递附加费', decimal_places=2, max_digits=14),
        ),
    ]
