from django.db import models
 
class Classes(models.Model):
    """
    班级表,男
    """
    title = models.CharField(max_length=32)
    m = models.ManyToManyField("Teachers")
 
class Teachers(models.Model):
    """
    老师表，女
    """
    name = models.CharField (max_length=32)
 
class Student(models.Model):
    username = models.CharField(max_length=32)
    age = models.IntegerField()
    gender = models.BooleanField()
    cs = models.ForeignKey(Classes)
    
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)

class Transport_way(models.Model):
    transport_way = models.CharField(max_length=32,verbose_name="货运方式",null=False)

class Clearance_sign(models.Model):
    clearance_sign = models.CharField(max_length=32,verbose_name="通关符号",null=False)

class BuyingItem(models.Model):
    """
    基础资料
    """
    no = models.IntegerField(verbose_name="NO")
    item_no = models.CharField(max_length=32,verbose_name="商品编号",null=False)
    choice_name = models.CharField(max_length=200,verbose_name="选项",null=False)
    name = models.CharField(max_length=200,verbose_name="商品名称",null=False)
    #采购单价
    buying_price = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="采购单价")
    #表面价
    face_price = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="表面价")
    #加减金额
    add_price = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="加减金额")
    #国内运费
    native_trans_fee = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="国内运费")
    #实际售价
    price = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="实际售价")
    #国际物流费
    national_tran_fee = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="国际物流费")
    #平台手续费
    service_charge_rate = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="平台手续费")
    #手续费
    service_charge_fee = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="手续费")
    #利润
    profit  = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="利润")
    #中文品名
    chinese_kind_name = models.CharField(max_length=200,verbose_name="中文品名",null=False)
    #英文品名
    english_name = models.CharField(max_length=200,verbose_name="英文品名",null=False)
    #重量
    weight = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="重量")
    #体积
    volume = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="体积")
    #美金单价
    american_price = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="美金单价")
    #实际报关美金
    real_american_price = models.DecimalField(max_digits=14,decimal_places=2,null=False,verbose_name="实际报关美金")
    #HS编码
    hs_code = models.CharField(max_length=200,verbose_name="HS编码",null=False)
    #产品上传
    upload_day = models.DateField(auto_now=True,null=False,verbose_name="产品上传")
    #产品下架
    downshelf_day = models.DateField(verbose_name="产品下架")
    #剩余日
    leftdays = models.IntegerField(verbose_name="剩余日")
    #采购品名
    buying_name = models.CharField(max_length=200,verbose_name="采购品名",null=False)
    #采购地址
    buying_url = models.URLField(max_length=500,verbose_name="采购地址",null=False)
    #状态
    status = models.CharField(max_length=200,verbose_name="状态")
    #韩文名
    korea_name = models.CharField(max_length=200,verbose_name="状态",null=False)
    #中文名
    chinese_name = models.CharField(max_length=200,verbose_name="状态",null=False)
    #货运方式
    transport_way_id = models.ForeignKey(Transport_way,verbose_name="货运方式",related_name="transport_way_id",null=True)
    #通关符号
    clearance_sign_id = models.ForeignKey(Clearance_sign,verbose_name="通关符号",related_name="clearance_sign_id",null=True)
    #关税
    tariff = models.DecimalField(max_digits=14,decimal_places=2,verbose_name="关税")
    #快递附加费
    add_express_fee = models.DecimalField(max_digits=14,decimal_places=2,verbose_name="快递附加费",null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "采购单"
        verbose_name_plural = "采购单"
        ordering = ['item_no']


#---采购基础资料
# NO        no
# 商品编号   item_no
# 选项      choice_name
# 商品名称   name
# 采购单价   buying_price
# 表面价     face_price
# 加减金额    add_price
# 国内运费    native_trans_fee
# 实际售价    price
# 国际物流费  national_tran_fee
# 平台手续费  service_charge_rate
# 手续费      service_charge_fee
# 利润       profit
# 中文品名    chinese_name
# 英文品名    english_name
# 重量        weight
# 体积        volume
# 美金单价     american_price
# 实际报关美金  real_american_price
# HS编码       hs_code
# 产品上传      upload_day
# 产品下架      downshelf_day
# 剩余日       leftdays
# 采购品名      buying_name
# 采购地址      buying_url
# 状态          status
# 韩文名        korea_name
# 中文名        chinese_name
# 货运方式    transport_way
# 通关符号    clearance_sign
# 关税       tariff
# 快递附加费  add_express_fee
# 运输公司    transport_company