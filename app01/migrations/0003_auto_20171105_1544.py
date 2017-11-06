# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('no', models.IntegerField(verbose_name='NO')),
                ('item_no', models.CharField(verbose_name='商品编号', max_length=32)),
                ('choice_name', models.CharField(verbose_name='选项', max_length=200)),
                ('name', models.CharField(verbose_name='商品名称', max_length=200)),
                ('buying_price', models.DecimalField(decimal_places=2, verbose_name='采购单价', max_digits=14)),
                ('face_price', models.DecimalField(decimal_places=2, verbose_name='表面价', max_digits=14)),
                ('add_price', models.DecimalField(decimal_places=2, verbose_name='加减金额', max_digits=14)),
                ('native_trans_fee', models.DecimalField(decimal_places=2, verbose_name='国内运费', max_digits=14)),
                ('price', models.DecimalField(decimal_places=2, verbose_name='实际售价', max_digits=14)),
                ('national_tran_fee', models.DecimalField(decimal_places=2, verbose_name='国际物流费', max_digits=14)),
                ('service_charge_rate', models.DecimalField(decimal_places=2, verbose_name='平台手续费', max_digits=14)),
                ('service_charge_fee', models.DecimalField(decimal_places=2, verbose_name='手续费', max_digits=14)),
                ('profit', models.DecimalField(decimal_places=2, verbose_name='利润', max_digits=14)),
                ('english_name', models.CharField(verbose_name='英文品名', max_length=200)),
                ('weight', models.DecimalField(decimal_places=2, verbose_name='重量', max_digits=14)),
                ('volume', models.DecimalField(decimal_places=2, verbose_name='体积', max_digits=14)),
                ('american_price', models.DecimalField(decimal_places=2, verbose_name='美金单价', max_digits=14)),
                ('real_american_price', models.DecimalField(decimal_places=2, verbose_name='实际报关美金', max_digits=14)),
                ('hs_code', models.CharField(verbose_name='HS编码', max_length=200)),
                ('upload_day', models.DateField(auto_now=True, verbose_name='产品上传')),
                ('downshelf_day', models.DateField(verbose_name='产品下架')),
                ('leftdays', models.IntegerField(verbose_name='剩余日')),
                ('buying_name', models.CharField(verbose_name='采购品名', max_length=200)),
                ('buying_url', models.URLField(verbose_name='采购地址')),
                ('status', models.CharField(verbose_name='状态', max_length=200)),
                ('korea_name', models.CharField(verbose_name='状态', max_length=200)),
                ('chinese_name', models.CharField(verbose_name='状态', max_length=200)),
                ('tariff', models.DecimalField(decimal_places=2, verbose_name='关税', max_digits=14)),
                ('add_express_fee', models.DecimalField(decimal_places=2, verbose_name='快递附加费', max_digits=14)),
            ],
            options={
                'ordering': ['item_no'],
                'verbose_name': '采购单',
                'verbose_name_plural': '采购单',
            },
        ),
        migrations.CreateModel(
            name='Clearance_sign',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('clearance_sign', models.CharField(verbose_name='通关符号', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Transport_company',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('transport_company', models.CharField(verbose_name='运输公司', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Transport_way',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('transport_way', models.CharField(verbose_name='货运方式', max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='buyingitem',
            name='clearance_sign_id',
            field=models.ForeignKey(related_name='clearance_sign_id', to='app01.Transport_way', verbose_name='通关符号'),
        ),
        migrations.AddField(
            model_name='buyingitem',
            name='transport_company_id',
            field=models.ForeignKey(related_name='transport_company_id', to='app01.Transport_way', verbose_name='运输公司'),
        ),
        migrations.AddField(
            model_name='buyingitem',
            name='transport_way_id',
            field=models.ForeignKey(related_name='transport_way_id', to='app01.Transport_way', verbose_name='货运方式'),
        ),
    ]
